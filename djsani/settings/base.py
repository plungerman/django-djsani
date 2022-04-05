# -*- coding: utf-8 -*-

"""Django settings for project."""

import datetime
import os

# sqlserver connection string
from djimix.settings.local import DBSERVERNAME
from djimix.settings.local import INFORMIX_ODBC
from djimix.settings.local import INFORMIX_ODBC_TRAIN
from djimix.settings.local import INFORMIXDIR
from djimix.settings.local import INFORMIXSERVER
from djimix.settings.local import INFORMIXSQLHOSTS
from djimix.settings.local import LD_LIBRARY_PATH
from djimix.settings.local import LD_RUN_PATH
from djimix.settings.local import MSSQL_EARL
from djimix.settings.local import ODBCINI
from djimix.settings.local import ONCONFIG


# Debug
DEBUG = False
INFORMIX_DEBUG = ''
ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS
SECRET_KEY = ''
ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
]
ALLOWED_IMAGE_EXTENSIONS = (
    'jpg', 'jpeg', 'heic', 'pdf', 'png', 'JPG', 'JPEG', 'HEIC', 'PDF', 'PNG',
)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = True
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
FILE_UPLOAD_PERMISSIONS = 0o644
ROOT_URLCONF = 'djsani.core.urls'
SERVER_URL = ''
API_URL = ''
LIVEWHALE_API_URL = ''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(__file__)
ROOT_URL = '/medical-forms/'
MEDIA_ROOT = '{0}/assets/'.format(BASE_DIR)
MEDIA_URL = '/media/djsani/'
STATIC_ROOT = '{0}/static/'.format(ROOT_DIR)
STATIC_URL = 'https://{0}/static/djsani/'.format(SERVER_URL)
UPLOADS_DIR = '{0}files/'.format(MEDIA_ROOT)
UPLOADS_URL = '{0}files/'.format(MEDIA_URL)
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_djsani',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
    },
    'informix': {
        'ENGINE': 'django_informixdb',
        'NAME': '',
        'SERVER': '',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {
            'DRIVER': '/opt/ibm/informix/lib/cli/iclit09b.so',
            'CPTIMEOUT': 120,
            'CONN_TIMEOUT': 120,
            'ISOLATION_LEVEL': 'READ_UNCOMMITTED',
            'LOCK_MODE_WAIT': 0,
            'VALIDATE_CONNECTION': True,
        },
        'CONNECTION_RETRY': {
            'MAX_ATTEMPTS': 10,
        },
        'TEST': {
            'NAME': '',
            'CREATE_DB': False,
        },
    },
}
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djsani.core',
    'djsani.emergency',
    'djsani.insurance',
    'djsani.medical_history',
    'djsani.medical_history.waivers',
    'djtools',
    # third party apps
    'loginas',
    # honeypot for admin attacks
    'admin_honeypot',
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Add the automatic auth middleware just after the default
    # AuthenticationMiddleware that manages sessions and cookies
    # 'djauth.middleware.AutomaticUserLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # the following should be uncommented unless you are
    # embedding your apps in iframes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            '/data2/django_templates/djkali/',
            '/data2/django_templates/djcher/',
            '/data2/django_templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = None
LDAP_OBJECT_CLASS = ''
LDAP_GROUPS = None
LDAP_RETURN = ()
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_NAME = ''
SESSION_COOKIE_AGE = 86400
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_SSL_REDIRECT = True
# app settings
INSURANCE_RECIPIENTS = []
INSURANCE_GROUP_NUMBER = ''
HOUSING_EMAIL_LIST = []
HARM_EMAIL_LIST = []
UPLOAD_EMAIL_DICT = {}
DEFAULT_HASH = ''
DEFAULT_CID = '666'
START_DATE = datetime.datetime(datetime.datetime.now().year, 6, 1)
DECEMBER = 12
ADULT_AGE = 18
SPORTS_MONTH = 5
ACADEMIC_YEAR_LIMBO = False
STAFF_GROUP = 'MedicalStaff'
COACH_GROUP = 'AthleticsCoach'
TEST_STUDENT_ID = None
TEST_STAFF_ID = None
ROTATE_PHOTO = -90
# logging
LOG_FILEPATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/',
)
LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
DEBUG_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
INFO_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'info.log')
ERROR_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'error.log')
CUSTOM_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'custom.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'custom_logfile': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'filters': ['require_debug_true'],  # don't run logger in production
            'class': 'logging.FileHandler',
            'filename': CUSTOM_LOG_FILENAME,
            'formatter': 'custom',
        },
        'info_logfile': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10,
            'maxBytes': 50000,
            'filters': ['require_debug_false'],  # run logger in production
            'filename': INFO_LOG_FILENAME,
            'formatter': 'simple',
        },
        'debug_logfile': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'error_logfile': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'filters': ['require_debug_true'],  # don't run logger in production
            'class': 'logging.FileHandler',
            'filename': ERROR_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'djauth': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
