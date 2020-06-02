# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys

from django.core.wsgi import get_wsgi_application


# python
sys.path.append('/d2/python_venv/3.6/djsani/lib/python3.6/')
sys.path.append('/d2/python_venv/3.6/djsani/lib/python3.6/site-packages/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.staging')
os.environ.setdefault('PYTHON_EGG_CACHE', '/var/cache/python/.python-eggs')
os.environ.setdefault('TZ', 'America/Chicago')
# informix
os.environ['INFORMIXSERVER'] = 'wilson'
os.environ['DBSERVERNAME'] = 'wilson'
os.environ['INFORMIXDIR'] = '/opt/ibm/informix'
os.environ['ODBCINI'] = '/etc/odbc.ini'
#os.environ['ONCONFIG'] = 'onconf.cars'
os.environ['ONCONFIG'] = 'onconf.train'
os.environ['INFORMIXSQLHOSTS'] = '/opt/ibm/informix/etc/sqlhosts'
os.environ['LD_LIBRARY_PATH'] = """
    {0}/lib:{0}/lib/esql:{0}/lib/tools:/usr/lib/apache2/modules:{0}/lib/cli
""".format(os.environ['INFORMIXDIR'])
os.environ['LD_RUN_PATH'] = os.environ['LD_LIBRARY_PATH']
# wsgi
application = get_wsgi_application()
