# -*- coding: utf-8 -*-
from django.urls import (
    re_path,
    include
)

urlpatterns = [
    # api_v1
    re_path(r'^api/v1/', include(('api.v1.urls', 'api.v1'), namespace='v1')),
]
