"""
WSGI config for Musetic.
"""

import os

from django.core.wsgi import get_wsgi_application

from musetic.settings.utils import get_env_variable

try:
    from dj_static import Cling
except ImportError:
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_env_variable('DJANGO_SETTINGS_MODULE'))

if get_env_variable('DJANGO_SETTINGS_MODULE') == 'musetic.settings.production':
    application = Cling(get_wsgi_application())
else:
    application = get_wsgi_application()
