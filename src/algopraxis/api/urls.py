# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    # Problem's views
    url(r'^$', views.ProblemListAPIView.as_view(), name='list'),
    url(r'^create/$', views.ProblemCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProblemDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', views.ProblemUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.ProblemDeleteAPIView.as_view(), name='delete'),
    # Solution's views
    url(r'^(?P<slug>[\w-]+)/solution/$', views.SolutionDetailAPIView.as_view(), name='solution-detail'),
    url(r'^(?P<slug>[\w-]+)/solution/create/$', views.SolutionCreateAPIView.as_view(), name='solution-create'),
    url(r'^(?P<slug>[\w-]+)/solution/update/$', views.SolutionUpdateAPIView.as_view(), name='solution-update'),
]