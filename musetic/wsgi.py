"""
WSGI config for Musetic.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from musetic.settings.utils import get_env_variable

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_env_variable('DJANGO_SETTINGS_MODULE'))

from django.core.wsgi import get_wsgi_application

if 'production' in get_env_variable('DJANGO_SETTINGS_MODULE'):
  from dj_static import Cling
  application = Cling(get_wsgi_application())
else:
  application = get_wsgi_application()
