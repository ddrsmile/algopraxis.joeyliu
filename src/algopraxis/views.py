# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Problem, Solution, TestCase
from .forms import ProblemForm, SolutionForm, TestCaseForm


class ProblemListView(View):
    def get(self, request, *args, **kwargs):
        problems = Problem.objects.all()
        paginator = Paginator(problems, 20)
        page = request.GET.get('page')
        try:
            problems = paginator.page(page)
        except PageNotAnInteger:
            problems = paginator.page(1)
        except EmptyPage:
            problems = paginator.page(paginator.num_pages)

        context = {'problems': problems}
        template = 'algopraxis/problem/list.html'
        return render(request, template, context)

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
        problem = get_object_or_404(Problem, user=request.user, slug=slug)
        solution = problem.solutions.first()
        testcase = problem.testcases.first()
        solution_form = SolutionForm(instance=solution)
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
            return Http404
        problem = get_object_or_404(Problem, user=request.user, slug=slug)
        solution = problem.solutions.first()
        solution_form = SolutionForm(request.POST, instance=solution)
        if solution_form.is_valid():
            solution = solution_form.save(commit=False)
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
            return Http404
        problem = get_object_or_404(Problem, user=request.user, slug=slug)
        solution = problem.solutions.first()
        testcase = problem.testcases.first()
        solution_form = SolutionForm(instance=solution)
        testcase_form = TestCaseForm(request.POST, instance=testcase)
        if testcase_form.is_valid():
            testcase = testcase_form.save(commit=False)
            if not testcase.problem_id:
                testcase.problem = problem
            testcase.save()
            messages.success(request, "Test cases has been successfully updated...")
            return HttpResponseRedirect(problem.get_abs_url())
        else:
            messages.error(request, "Test cases was not updated successfully...")
            context = {
                'problem': problem,
                'solution_form': solution_form,
                'testcase_form': testcase_form
            }
            template = 'algopraxis/problem/detail.html'

            return render(request, template, context)