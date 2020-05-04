# -*- coding: utf-8 -*-
import json
from .default import *

with open('/usr/local/etc/webapps.json') as f:
    config = json.load(f)

SECRET_KEY = config["SECRET_KEY"]
ALLOWED_HOSTS = ['*']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'algopraxis',
        'USER': config['DB']['USER'],
        'PASSWORD': config['DB']['PASSWORD'],
        'HOST': config['DB']['HOST'],
        'PORT': config['DB']['PORT'],
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
    },
}
