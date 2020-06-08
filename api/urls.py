# -*- coding: utf-8 -*-
from django.urls import (
    re_path,
    include
)

urlpatterns = [
    # auth
    re_path(r'^auth/', include(('api.auth.urls', 'api.auth'), namespace='auth')),
    # api_v1
    re_path(r'^v1/', include(('api.v1.urls', 'api.v1'), namespace='v1')),
]
