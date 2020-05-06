# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # problems
    url(r'^problems$', views.ProblemListAPIView.as_view(), name='problem_list'),
    url(r'^problems/create$', views.ProblemCreateAPIView.as_view(), name='problem_create'),
    url(r'^problems/(?P<pk>[\d]+)$', views.ProblemRUDAPIView.as_view(), name='problem_rud'),
    url(r'^problems/(?P<pk>[\d]+)/detail$', views.ProblemDetailAPIView.as_view(), name='problem_detail'),

    # code_set
    url(r'^codesets/create$', views.CodeSetCreateAPIView.as_view(), name='code_set_create'),
    url(r'^codesets/(?P<pk>[\d]+)$', views.CodeSetRUDAPIView.as_view(), name='code_set_rud'),

    # solutions
    url(r'^solutions/create$', views.SolutionCreateAPIView.as_view(), name='solution_create'),
    url(r'^solutions/(?P<pk>[\d]+)$', views.SolutionRUDAPIView.as_view(), name='solution_rud'),

    # executor
    url(r'^execute$', views.ExecuteAPIView.as_view(), name='execute'),
]