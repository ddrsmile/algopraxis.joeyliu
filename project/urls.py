# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.urls import (
    re_path,
    include
)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include(('api.urls', 'api'), namespace='api')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)