from .base import *
from musetic.settings.utils import get_env_variable
import dj_database_url

SECRET_KEY = get_env_variable('SECRET_KEY')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ALLOWED_HOSTS = ['*']

# Production Apps
INSTALLED_APPS += (
    'storages',
    's3_folder_storage',
)

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'joshchandler'
EMAIL_HOST_PASSWORD = 'J6NDSOF0N3'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@musetic.com'

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'musetic-caching.rrfsem.cfg.use1.cache.amazonaws.com:11211',
    }
}

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# Databases
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Queues
BROKER_TRANSPORT = 'redis'
BROKER_URL = get_env_variable('BROKER_URL', 'redis://localhost:6379/0')

CELERY_DEFAULT_QUEUE = 'musetic-prod'
CELERY_ALWAYS_EAGER = False

# Static and Media

DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = 'media'
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = 'static'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY  = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = '//s3.amazonaws.com/%s/new/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = '/%s/' % STATIC_S3_PATH
STATIC_URL = '//s3.amazonaws.com/%s/new/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
