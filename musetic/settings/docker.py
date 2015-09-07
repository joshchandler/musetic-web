
from .development import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'database',
        'PORT': '5432',
    }
}

BROKER_URL = get_env_variable('BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_ALWAYS_EAGER = bool(get_env_variable('CELERY_ALWAYS_EAGER', False))