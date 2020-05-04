# -*- coding: utf-8 -*-
from .base import *

ALLOWED_HOSTS = ['*']
DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
