from .common import *

DEBUG = False
ALLOWED_HOSTS = ['*']

STATICFILES_STORAGE = 'cogether.storages.StaticAzureStorage'
DEFAULT_FILE_STORAGE = 'cogether.storages.MediaAzureStorage'

AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    },
}

