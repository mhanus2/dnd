from .base import *

# todo - secret key
import os
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*']

DEBUG = False

# todo - database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dnd',                      
        'USER': 'dude',
        'PASSWORD': 'dude',
        'HOST': '127.0.0.1',
        'PORT': '5433',
    }
}


