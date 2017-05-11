# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Problem, Solution, TestCase
from .forms import ProblemForm, SolutionForm, TestCaseForm


class AlgopraxisView(View):
    def get(self, request, *args, **kwargs):
        probs = Problem.objects.all()

        tag = request.GET.get('tag')

        if tag:
            probs = probs.filter(tags__name=tag)

        paginator = Paginator(probs, 6)
        page = request.GET.get('page')
        try:
            probs = paginator.page(page)
        except PageNotAnInteger:
            probs = paginator.page(1)
        except EmptyPage:
            probs = paginator.page(paginator.num_pages)

        context = {'probs': probs}
        template = 'alogpraxis/problem_list.html'
        return render(request, template, context)

class ProblemCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        form = ProblemForm()
        context = {'form': form}
        template = 'alogpraxis/problem_form.html'
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
            template = 'alogpraxis/problem_form.html'
            return render(request, template, context)

class ProblemUpdateView(View):
    def get(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        problem = get_object_or_404(Problem, slug=slug)
        form = ProblemForm(instance=problem)
        context = { 'form': form }
        template = 'alogpraxis/problem_form.html'

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
            template = 'alogpraxis/problem_form.html'
            return render(request, template, context)

class ProblemDeleteView(View):
    def get(self, request, *args, slug=None, **kwargs):
        problem = get_object_or_404(Problem, slug=slug)
        problem.delete()
        messages.success(request, "Problem has been deleted successfully...")
        return redirect('problem:list')

class ProblemDetail(View):
    def get(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        problem = get_object_or_404(Problem, slug=slug)
        form = SolutionForm()
        context = {
            'problem': problem,
            'form': form
        }
        template = 'alogpraxis/problem_detail.html'

        return render(request, template, context)

class SolutionSaveView(View):
    def post(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http404
        problem = get_object_or_404(Problem, user=request.user, slug=slug)
        solution = problem.solutions.first()
        form = SolutionForm(request.POST, instance=solution)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.save()
            messages.success(request, "Solution has been successfully updated...")
            return HttpResponseRedirect(problem.get_abs_url())
        else:
            messages.error(request, "Problem was not updated successfully...")
            context = {
                'problem': problem,
                'form': form
            }
            template = 'alogpraxis/problem_detail.html'

            return render(request, template, context)

