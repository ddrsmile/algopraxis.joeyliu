# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Problem, Solution, TestCase
from .forms import ProblemForm, SolutionForm, TestCaseForm

from coderunner.src.runner import Runner

class SinginView(View):
    def get(self, request):
        next = request.GET.get('next', '/')
        context = {'next': next}
        template = 'algopraxis/signin.html'
        return render(request, template, context)

    def post(self, request):
        user = request.user
        next = request.GET.get('next', '/')
        if not user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            context = {'next': next}
            template = 'algopraxis/signin.html'
            context['emsg'] = "You must have an account to use ALGOPRAXIS!!"
            return render(request, template, context)

class SingoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        template = 'algopraxis/home.html'
        return render(request, template, context)

class AboutView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        template = 'algopraxis/about.html'
        return render(request, template, context)

class ProblemListView(generic.ListView):
    model = Problem
    context_object_name = "problems"
    template_name = 'algopraxis/problem/list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ProblemListView, self).get_context_data(**kwargs)

        page = context.get('page_obj')
        paginator = context.get('paginator')
        customized_range = self.designate_pages_range(page, paginator)
        context.update(customized_range)

        return context

    def designate_pages_range(self, page, paginator):
        start_index = max(1, page.number - 2)
        end_index = min(start_index + 4, paginator.num_pages)

        start_index = min(start_index, max(end_index - 4, 1))

        customized_range = [i for i in range(start_index, end_index + 1)]
        return {'customized_range':customized_range}


class ProblemTaggedListView(View):
    def get(self, request, tag=None, *args, **kwargs):
        problems = Problem.objects.all()
        problems.filter(tags__name=tag)
        context = {'tag': tag, 'problems': problems}
        template = 'algopraxis/problem/tagged_list.html'
        return render(request, template, context)

class ProblemCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        form = ProblemForm()
        context = {'form': form}
        template = 'algopraxis/problem/form.html'
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        form = ProblemForm(request.POST)
        if form.is_valid():
            new_prob = form.save(commit=False)
            new_prob.save()
            messages.success(request, "Problem has been successfully created...")
            return HttpResponseRedirect(new_prob.get_abs_url())
        else:
            messages.error(request, "Problem was not created successfully...")
            context = {'form': form}
            template = 'algopraxis/problem/form.html'
            return render(request, template, context)

class ProblemUpdateView(View):
    def get(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        problem = get_object_or_404(Problem, slug=slug)
        form = ProblemForm(instance=problem)
        context = { 'form': form }
        template = 'algopraxis/problem/form.html'

        return render(request, template, context)

    def post(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        problem = get_object_or_404(Problem, slug=slug)
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.save()
            messages.success(request, "Problem has been successfully updated...")
            return HttpResponseRedirect(problem.get_abs_url())
        else:
            messages.error(request, "Problem was not updated successfully...")
            context = {'form': form}
            template = 'algopraxis/problem/form.html'
            return render(request, template, context)

class ProblemDeleteView(View):
    def get(self, request, *args, slug=None, **kwargs):
        problem = get_object_or_404(Problem, slug=slug)
        problem.delete()
        messages.success(request, "Problem has been deleted successfully...")
        return redirect('algopraxis:list')

class ProblemDetail(View):
    def get(self, request, slug=None, *args, **kwargs):
        problem = get_object_or_404(Problem, slug=slug)
        solution = problem.solutions.first()
        testcase = problem.testcases.first()
        solution_form = SolutionForm(instance=solution) if solution else SolutionForm(initial={'code': problem.solution_start_code})
        testcase_form = TestCaseForm(instance=testcase)
        context = {
            'problem': problem,
            'solution_form': solution_form,
            'testcase_form': testcase_form
        }
        template = 'algopraxis/problem/detail.html'

        return render(request, template, context)

class SolutionSaveView(View):
    def post(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            emsgs = json.dumps('The user is invalid!!')
            return HttpResponse(emsgs, status=404, content_type='application/json')
        problem = get_object_or_404(Problem, slug=slug)
        solution = problem.solutions.first()
        solution_form = SolutionForm(request.POST, instance=solution)
        if solution_form.is_valid():
            solution = solution_form.save(commit=False)
            if not solution.user_id:
                solution.user = request.user
            if not solution.problem_id:
                solution.problem = problem
            solution.save()
            return HttpResponse({})
        else:
            emsgs = json.dumps(solution_form.errors)
            return HttpResponse(emsgs, status=400, content_type='application/json')

class TestCaseSaveView(View):
    def post(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            emsgs = json.dumps('The user is invalid!!')
            return HttpResponse(emsgs, status=404, content_type='application/json')
        problem = get_object_or_404(Problem, slug=slug)
        testcase = problem.testcases.first()
        testcase_form = TestCaseForm(request.POST, instance=testcase)
        if testcase_form.is_valid():
            testcase = testcase_form.save(commit=False)
            if not testcase.problem_id:
                testcase.problem = problem
            testcase.save()
            return HttpResponse({})
        else:
            emsgs = json.dumps(testcase_form.errors)
            return HttpResponse(emsgs, status=400, content_type='application/json')

class RunView(View):
    def post(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            emsgs = json.dumps('The user is invalid!!')
            return HttpResponse(emsgs, status=404, content_type='application/json')
        problem = get_object_or_404(Problem, slug=slug)
        main_content = problem.main_file_code
        sol_content = request.POST.get('code')
        input_data = request.POST.get('testcases')

        runner = Runner()
        runner.set_files(main_content, sol_content, input_data)
        outputs = runner.run()
        to_json = {}
        for i, output in enumerate(outputs):
            to_json[i] = output
        return JsonResponse(to_json)
