import os

from .base import *

SECRET_KEY = 'django-insecure-455p9io@)pkf_ly#g^ihns1d#1ufgexx(0(mxxs^ppuoj4uim)'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}
