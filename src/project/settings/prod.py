from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# static path
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

try:
    from .local import *
except ImportError:
    pass
