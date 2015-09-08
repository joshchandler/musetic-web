"""
WSGI config for Musetic.
"""

import os
from musetic.settings.utils import get_env_variable

try:
    from dj_static import Cling
except ImportError:
    pass
  
django_settings = get_env_variable('DJANGO_SETTINGS_MODULE')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_env_variable('DJANGO_SETTINGS_MODULE'))

from django.core.wsgi import get_wsgi_application

if get_env_variable('DJANGO_SETTINGS_MODULE') == 'musetic.settings.production':
    from dj_static import Cling  # pragma 
    application = Cling(get_wsgi_application())
else:
    application = get_wsgi_application()
