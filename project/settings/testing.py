# -*- coding: utf-8 -*-
from .default import *

SECRET_KEY = 'kmIuhfK^k+}C^b#@F6236G<L)Js)>1OyQ5~DEY@zn[zWw[]ClJ%4D?):#rOtx$M7'
ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'testing.sqlite3'),
        }
    }
}

# django-redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
