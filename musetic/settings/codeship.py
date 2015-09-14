from .base import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


SECRET_KEY = get_env_variable('SECRET_KEY')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'tmp')
DEFAULT_FROM_EMAIL = 'no-reply@musetic.com'

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

# CACHING
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://localhost:6379',
    }
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': os.environ.get('PG_USER'),
        'PASSWORD': os.environ.get('PG_PASSWORD'),
        'HOST': '127.0.0.1',
        }
}

# STATIC AND MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

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


