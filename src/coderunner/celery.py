from __future__ import absolute_import
from celery import Celery
from django.conf import settings

app = Celery('coderunner')
app.config_from_object(settings)
