import djcelery
import os
import re
from datetime import timedelta
from django import contrib
from django.utils.http import urlquote

# Django settings for uptee project.

djcelery.setup_loader()

PROJECT_DIR = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PROJECT_DIR + '/database.db',    # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PROJECT_DIR, 'cache'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Paginator
PAGINATION_DEFAULT_PAGINATION = 20
# ... 2 3 4 [5] 6 7 8 ...
PAGINATION_DEFAULT_WINDOW = 3
# If the last page has 1 object, the object gets attached to previous one instead.
PAGINATION_DEFAULT_ORPHANS = 1
PAGINATION_INVALID_PAGE_RAISES_404 = True

# Gravatar default image
GRAVATAR_DEFAULT_IMAGE = 'mm'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# The next line is necessary for production settings
#STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(contrib.__path__[0], 'admin', 'static'),
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'oj^cv)^5b^a1ke-%d8-7$5$k5)sj70w8d97b3z!mvamgd#a0tl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'lib.template_loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_pybrowscap.middleware.PybrowscapMiddleware',
    'lib.template_middleware.TemplateMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'mod.context_processors.mod',
    'lib.context_processors.settings',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

AVAILABLE_TEMPLATES = (
    ('simpleblue', 'SimpleBlue', True),
    ('simpleflat', 'SimpleFlat', False)
)

DEFAULT_TEMPLATE = 'simpleblue'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django_comments',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_pybrowscap',
    'testingstate',
    'lib',
    'econ',
    'crumbs',
    'djcelery',
    'pagination',
    'mod',
    'accounts',
    'blog',
    'my_comments',
    'messaging',
    'captcha',
    'gravatar',
)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/users/{0}/".format(urlquote(o.username))
}

TESTING_STATE = False

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

# mail dummy
SERVER_EMAIL = ''

# user profile
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
COMMENTS_APP = 'my_comments'

# teeworlds executable
SERVER_EXEC = 'teeworlds_srv'

# Broker URL for celery
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

# celery scheduled tasks
CELERYBEAT_SCHEDULE = {
    # every minutes
    'check_server_state': {
        'task': 'mod.tasks.check_server_state',
        'schedule': timedelta(seconds=30)
    },
}

CELERY_TIMEZONE = 'UTC'

# This setting will effectively turn the middleware off, to speed up requests/response while developing
#PYBROWSCAP_INITIALIZE = True # Default is `not settings.DEBUG`.

# Path where browscap file is located on filesystem
PYBROWSCAP_FILE_PATH = os.path.join(PROJECT_DIR, 'browscap.csv')  # Default is '' (empty string) (copy browscap.csv.example to browscap.csv)

# Whether to perform automatic updates of browscap file
PYBROWSCAP_UPDATE = True  # Default is False

# Interval of automatic browscap file updates
PYBROWSCAP_UPDATE_INTERVAL = 604800  # Default one week in seconds

# Tuple or regex expressions of path that are to be ignored by middleware
PYBROWSCAP_IGNORE_PATHS = (
    re.compile(r'^/favicon.ico$'),
    re.compile(r'^/media/'),
    re.compile(r'^/static/')
)  # Default empty tupple
