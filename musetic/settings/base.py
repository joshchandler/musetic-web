"""
Django settings for musetic project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from .logging import *
from musetic.settings.utils import get_env_variable
from datetime import timedelta
import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(BASE_DIR))

# INSTALLED APPS

DJANGO_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django_extensions',
)
UNIVERSE_APPS = (
    # Third-party apps
    'djcelery',
    'celery',
    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'social.apps.django_app.default',
    'crispy_forms',
    'crispy_forms_foundation',
    'appconf',
    'markdown_deux',
)

PROJECT_APPS = (
    # Musetic apps
    'musetic.apps.avatar',
    'musetic.apps.discussion',
    'musetic.apps.submission',
    'musetic.apps.user',

)

INSTALLED_APPS = DJANGO_APPS + UNIVERSE_APPS + PROJECT_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'musetic.urls'

WSGI_APPLICATION = 'musetic.wsgi.application'

CRISPY_TEMPLATE_PACK = 'foundation-5'

# Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# COMMENTS

COMMENTS_APP = 'musetic.apps.discussion'


# TEMPLATES

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# STATIC/MEDIA

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# AUTHENTICATION

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True


# SOCIAL AUTH

SOCIAL_AUTH_PIPELINE = (

    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.get_username',
    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGOUT_URL = '/logout/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_KEY = '290635347808167'
SOCIAL_AUTH_FACEBOOK_SECRET = '560bee0c1ccc8f962a827cb4ac7d01c3'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '911284089968-86bdqh47c9lqoke5daut8oit65r7odru.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'TS2L7U1BwCjfAYnWnWZECfM_'


# CELERY

# Broker
BROKER_TRANSPORT = 'redis'
BROKER_URL = get_env_variable('BROKER_URL', 'redis://localhost:6379/0')
BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True
}
# Queues
CELERY_DEFAULT_QUEUE = 'musetic-dev'
# Results
CELERY_RESULT_BACKEND = BROKER_URL
# Events
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True

# make `.delay()` behave like `.run()` when this is True.
CELERY_ALWAYS_EAGER = bool(get_env_variable('CELERY_ALWAYS_EAGER', True))
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYBEAT_SCHEDULE = {
    'rank-all-submissions': {
        'task': 'musetic.apps.submission.tasks.RankAllSubmissionsTask',
        'schedule': timedelta(minutes=1),
    },
}

CELERY_TIMEZONE = 'UTC'

DEFAULT_FROM_EMAIL = 'noreply@musetic.com'
