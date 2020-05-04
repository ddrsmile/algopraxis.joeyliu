# -*- coding: utf-8 -*-
import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = ['celery_app', BASE_DIR]
