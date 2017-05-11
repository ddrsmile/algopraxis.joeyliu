# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AlgopraxisView.as_view(), name='list'),
    url(r'^create/$', views.ProblemCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProblemDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.ProblemUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.ProblemDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/save/$', views.SolutionSaveView.as_view(), name='save'),
]