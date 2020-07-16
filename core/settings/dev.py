from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%$^=hk%5n$=v=&ibd49_jqvy#83s3y%!a$%jp6#v2mjw__28ro'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    'rest_framework',
]

try:
    from .local import *
except ImportError:
    pass
