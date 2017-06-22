from __future__ import absolute_import, unicode_literals

from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'algopraxis.joeyliu.dev']

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

try:
    from .local import *
except ImportError:
    pass
