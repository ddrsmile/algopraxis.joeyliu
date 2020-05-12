# -*- coding: utf-8 -*-
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'token/acquire', views.token_acquire_api_view, name='token_acquire'),
    re_path(r'token/refresh', views.token_refresh_api_view, name='token_refresh'),
    re_path(r'token/invalidate', views.token_invalidate_api_view, name='token_invalidate'),
]
