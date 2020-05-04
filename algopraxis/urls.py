# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^signin/$', views.SignInView.as_view(), name='signin'),
    url(r'^signout/$', views.SingoutView.as_view(), name='signout'),
    url(r'^problems/$', views.ProblemListView.as_view(), name='list'),
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^api/', include(('algopraxis.api.urls', 'algopraxis.api'), namespace='api')),
    url(r'^create/$', views.ProblemCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProblemDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.ProblemEditView.as_view(), name='edit'),
]