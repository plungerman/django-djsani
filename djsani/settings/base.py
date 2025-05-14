# -*- coding: utf-8 -*-

"""Django settings for project."""

import datetime
import os

# Debug
DEBUG = False
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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_APP = os.path.basename(BASE_DIR)
ROOT_URLCONF = 'djsani.core.urls'
SERVER_URL = ''
DIRECTORY_API_URL = 'https://{0}/{1}'.format(SERVER_URL, 'directory/api/')
LIVEWHALE_API_URL = ''
ROOT_DIR = os.path.dirname(__file__)
ROOT_URL = '/medical-forms/'
MEDIA_ROOT = '{0}/assets/'.format(BASE_DIR)
MEDIA_URL = '/media/{0}/'.format(PROJECT_APP)
STATIC_ROOT = '{0}/static/'.format(ROOT_DIR)
STATIC_URL = 'https://{0}/static/{1}/'.format(SERVER_URL, PROJECT_APP)
UPLOADS_DIR = '{0}files/'.format(MEDIA_ROOT)
UPLOADS_URL = '{0}files/'.format(MEDIA_URL)
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_{0}'.format(PROJECT_APP),
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
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
    # 2FA auth with saml2
    'django_saml',
    # apps
    'djsani.core',
    'djsani.insurance',
    'djsani.medical_history',
    'djsani.medical_history.waivers',
    # form forge
    'bootstrap4',
    # tools
    'djtools',
    # gmail api for send mail
    'gmailapi_backend',
    # third party apps
    'loginas',
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 86400,
        'KEY_PREFIX': '{0}_'.format(PROJECT_APP),
    }
}
'''
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
    'djauth.saml.backends.OneloginBackend',
    'djauth.backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# SAML settings
SAML_DEBUG = False
SAML_STRICT = False
SAML_LOGIN_REDIRECT = ROOT_URL
SAML_LOGOUT_REDIRECT = ROOT_URL
SAML_USERNAME_ATTR = ''
SAML_CID_ATTR = ''
SAML_CREATE_USER = True
SAML_UPDATE_USER = True
SAML_IDP_URL = 'https://{0}/{1}/saml/metadata/'.format(SERVER_URL, PROJECT_APP)
SAML_SECURITY = {
    'nameIdEncrypted': False,
    'authnRequestsSigned': False,
    'logoutRequestSigned': False,
    'logoutResponseSigned': False,
    'signMetadata': False,
    'wantMessagesSigned': False,
    'wantAssertionsSigned': False,
    'wantNameId' : True,
    'wantNameIdEncrypted': False,
    'wantAttributeStatement': False,
    'wantAssertionsEncrypted': False,
    'allowSingleLabelDomains': False,
    #'signatureAlgorithm': 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
    #'digestAlgorithm': 'http://www.w3.org/2001/04/xmlenc#sha256',
    'signatureAlgorithm': 'http://www.w3.org/2000/09/xmldsig#rsa-sha1',
    'digestAlgorithm': 'http://www.w3.org/2000/09/xmldsig#sha1'
}
SAML_CONTACT = {
    'technical': {
        'givenName': '',
        'emailAddress': '',
    },
    'support': {
        'givenName': '',
        'emailAddress': '',
    }
}
SAML_ORGANIZATION = {
    'en-US': {
        'name': '',
        'displayname': '',
        'url': '',
    }
}
SAML_SP = {
    'entityId': '',
    'assertionConsumerService': {
        'url': '',
        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'
    },
    'singleLogoutService': {
        'url': '',
        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
    },
    'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
}
# the x509cert value is from onelogin
SAML_IDP = {
    'entityId': '',
    'singleSignOnService': {
        'url': '',
        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
    },
    'singleLogoutService': {
        'url': '',
        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
    },
    'x509cert': ''
}
# saml_attr, django_attr
SAML_ATTR_MAP = [('', ''),]
SAML_ATTR_UPDATE_IGNORE = [('',)]
# vLDAP authentication (remove after saml2 integration)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_NAME = ''
SESSION_COOKIE_AGE = 86400
# gmail API settings
EMAIL_FROM = ''
GMAIL_USER = ''
EMAIL_BACKEND = 'gmailapi_backend.service.GmailApiBackend'
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
GMAIL_SERVICE_ACCOUNT_JSON = ''
GOOGLE_SERVICE_ACCOUNT = ''
# system email addresses
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = 'django_{0}_csrftoken'.format(PROJECT_APP)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_SSL_REDIRECT = True
# app settings
ROTATE_PHOTO = -90
# REST API AUTHENTICATION TOKEN
REST_FRAMEWORK_TOKEN = ''
INSURANCE_RECIPIENTS = []
INSURANCE_GROUP_NUMBER = ''
INSURANCE_COMPANY_NAME = ''
HOUSING_EMAIL_LIST = []
HARM_EMAIL_LIST = []
MENTAL_HEALTH_CHECK = []
UPLOAD_EMAIL_DICT = {}
WORKDAY_SPORTS_ROSTERS = ''
WORKDAY_USERNAME = ''
WORKDAY_PASSWORD = ''
# retry limit for requests package
WORKDAY_REQUESTS_RETRY = 100
# dates
START_DATE = datetime.datetime(datetime.datetime.now().year, 5, 1)
DECEMBER = 12
ADULT_AGE = 18
ACADEMIC_YEAR_LIMBO = False
# Groups
STAFF_GROUP = 'MedicalStaff'
COACH_GROUP = 'AthleticsCoach'
STUDENT_GROUP = 'carthageStudentStatus'
# testing
TEST_STUDENT_ID = None
TEST_STAFF_ID = None
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
