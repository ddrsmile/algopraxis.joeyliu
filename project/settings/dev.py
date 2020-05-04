# -*- coding: utf-8 -*-
from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
