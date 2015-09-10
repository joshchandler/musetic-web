from __future__ import absolute_import
from celery import Celery
from datetime import timedelta
from django.conf import settings

from musetic.settings.utils import get_env_variable


musetic_celery = Celery('musetic')
    

# Using a string here means the worker will not have to
# pickle the object when using Windows.
musetic_celery.config_from_object('django.conf:settings')
musetic_celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
musetic_celery.conf.update(
    BROKER_TRANSPORT='amqp',
    BROKER_TRANSPORT_OPTIONS={
        'fanout_prefix': True
    },
    CELERY_DEFAULT_QUEUE='musetic',
    CELERY_SEND_EVENTS=True,
    CELERY_SEND_TASK_SENT_EVENT=True,
    CELERY_ALWAYS_EAGER=bool(get_env_variable('CELERY_ALWAYS_EAGER', True)),
    CELERY_TIMEZONE='America/New_York',
    CELERY_ENABLE_UTC=True,
    CELERYBEAT_SCHEDULER='celery.beat:PersistentScheduler',
    CELERYBEAT_SCHEDULE={
        'rank-all-submissions': {
            'task': 'musetic.apps.submission.tasks.RankAllSubmissionsTask',
            'schedule': timedelta(minutes=1),
        }
    }
)


@musetic_celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
