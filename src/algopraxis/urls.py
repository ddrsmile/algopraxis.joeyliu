# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^signin/$', views.SinginView.as_view(), name='signin'),
    url(r'^signout/$', views.SingoutView.as_view(), name='signout'),
    url(r'^problems/$', views.ProblemListView.as_view(), name='list'),
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^tag/(?P<tag>[\w-]+)/$', views.ProblemTaggedListView.as_view(), name='tagged_list'),
    url(r'^api/', include('algopraxis.api.urls', namespace='api')),
    url(r'^create/$', views.ProblemCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProblemDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.ProblemUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.ProblemDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/save_solution/$', views.SolutionSaveView.as_view(), name='save_solution'),
    url(r'^(?P<slug>[\w-]+)/run/$', views.RunView.as_view(), name='run'),
]