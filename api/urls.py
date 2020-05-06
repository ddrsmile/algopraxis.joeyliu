# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [
    # api_v1
    url(r'^api/v1/', include(('api.v1.urls', 'api.v1'), namespace='algopraxis.api.v1')),
]
