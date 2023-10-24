# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys

from django.core.wsgi import get_wsgi_application


# python
sys.path.append('/d2/python_venv/3.10/djsani/lib/python/')
sys.path.append('/d2/python_venv/3.10/djsani/lib/python/site-packages/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')
os.environ.setdefault('PYTHON_EGG_CACHE', '/var/cache/python/.python-eggs')
os.environ.setdefault('TZ', 'America/Chicago')
# wsgi
application = get_wsgi_application()
