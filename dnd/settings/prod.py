from .base import *

# todo - secret key
import os
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

# todo - database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
