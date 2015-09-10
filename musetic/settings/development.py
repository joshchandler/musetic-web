from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

SECRET_KEY = '+uj8l**58(=^kg%1@x^#%vkqy3%3r883&^6azv59-z+6w%(+8('

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@musetic.com'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASS'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': '5432',
    }
}

# CELERY
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# STATIC AND MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PUBLIC_PATH, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = 'media'
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY  = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')

MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


