# -*- coding: utf-8 -*-
from .default import *

SECRET_KEY = 'kmIuhfK^k+}C^b#@F6236G<L)Js)>1OyQ5~DEY@zn[zWw[]ClJ%4D?):#rOtx$M7'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DEBUG = True

INSTALLED_APPS += [
    'api.tests'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'testing.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'testing.sqlite3'),
        }
    }
}
