"""
WSGI config for Musetic.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musetic.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
