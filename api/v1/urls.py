# -*- coding: utf-8 -*-
from django.urls import re_path
from . import views

urlpatterns = [
    # problems
    re_path(r'^problems$', views.ProblemListAPIView.as_view(), name='problem_list'),
    re_path(r'^problems/create$', views.ProblemCreateAPIView.as_view(), name='problem_create'),
    re_path(r'^problems/(?P<pk>[\d]+)$', views.ProblemRUDAPIView.as_view(), name='problem_rud'),
    re_path(r'^problems/(?P<pk>[\d]+)/detail$', views.ProblemDetailAPIView.as_view(), name='problem_detail'),

    # code_set
    re_path(r'^codesets/create$', views.CodeSetCreateAPIView.as_view(), name='code_set_create'),
    re_path(r'^codesets/(?P<pk>[\d]+)$', views.CodeSetRUDAPIView.as_view(), name='code_set_rud'),

    # solutions
    re_path(r'^solutions/create$', views.SolutionCreateAPIView.as_view(), name='solution_create'),
    re_path(r'^solutions/(?P<pk>[\d]+)$', views.SolutionRUDAPIView.as_view(), name='solution_rud'),

    # executor
    re_path(r'^execute$', views.ExecuteAPIView.as_view(), name='execute'),
]