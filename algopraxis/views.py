# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from .models import Problem


class SignInView(View):

    def get(self, request):
        _next = request.GET.get('next', '/')
        context = {'next': _next}
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


class ProblemListView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        template = 'algopraxis/problem/list.html'
        return render(request, template, context)


class ProblemCreateView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        template = 'algopraxis/problem/form.html'
        return render(request, template, context)


class ProblemEditView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        template = 'algopraxis/problem/form.html'
        return render(request, template, context)

class ProblemDetail(View):
    def get(self, request, slug=None):
        # check whether problem exists or not
        get_object_or_404(Problem, slug=slug)
        context = {}
        template = 'algopraxis/problem/detail.html'
        return render(request, template, context)