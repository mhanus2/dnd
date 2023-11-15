from .base import *

SECRET_KEY = 'django-insecure-455p9io@)pkf_ly#g^ihns1d#1ufgexx(0(mxxs^ppuoj4uim)'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.0.131', '192.168.0.129', '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

