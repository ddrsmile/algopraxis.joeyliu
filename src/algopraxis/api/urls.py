# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    # Problem's views
    url(r'^problems/$', views.ProblemListAPIView.as_view(), name='list'),
    url(r'^problems/create/$', views.ProblemCreateAPIView.as_view(), name='create'),
    url(r'^problems/(?P<slug>[\w-]+)/$', views.ProblemDetailAPIView.as_view(), name='detail'),
    url(r'^problems/(?P<slug>[\w-]+)/update/$', views.ProblemUpdateAPIView.as_view(), name='update'),
    url(r'^problems/(?P<slug>[\w-]+)/delete/$', views.ProblemDeleteAPIView.as_view(), name='delete'),
    # Solution's views
    url(r'^solution/(?P<id>\d+)/$', views.SolutionDetailAPIView.as_view(), name='solution-detail'),
    url(r'^solution/(?P<slug>[\w-]+)/create_or_update/(?P<lang_mode>[\w-]+)$', views.SolutionCreateUpdateAPIView.as_view(), name='solution-create-or-update'),
    #url(r'^solution/(?P<slug>[\w-]+)/create/$', views.SolutionCreateAPIView.as_view(), name='solution-create'),
    #url(r'^solution/(?P<id>\d+)/update/$', views.SolutionUpdateAPIView.as_view(), name='solution-update'),
    # CodeRunner
    url(r'^run/(?P<slug>[\w-]+)/$', views.RunAPIView.as_view(), name='run'),
]