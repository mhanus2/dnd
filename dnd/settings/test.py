from .base import *

# todo - secret key
SECRET_KEY = 'django-insecure-455p9io@)pkf_ly#g^ihns1d#1ufgexx(0(mxxs^ppuoj4uim)'

DEBUG = False

ALLOWED_HOSTS = []

# todo - database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
