from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from musetic.settings.utils import get_env_variable

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_env_variable('DJANGO_SETTINGS_MODULE'))

musetic_celery = Celery('musetic')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
musetic_celery.config_from_object('django.conf:settings')
musetic_celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
musetic_celery.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)


@musetic_celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
