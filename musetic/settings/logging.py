import os

LOG_LEVEL = os.environ.get('LOG_LEVEL')

if LOG_LEVEL not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
    LOG_LEVEL = 'INFO'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s %(levelname)s] %(name)s:L%(lineno)d \'%(message)s\'',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'musetic': {
            'handlers': ['console'],
            'filters': [],
            'level': LOG_LEVEL,
            'propagate': True,
        }
    }
}
