# pylint: disable-all
"""
settings_local.py

Change site-specific settings here.
"""

from settings_default import *

"""
There's a list of settings that you will probably override.
"""

"""
DEBUG

Turns Django into development mode.

Default: False
"""
DEBUG = True

"""
TEMPLATE_DEBUG

Additional debug data for templates.

Default: False
"""
TEMPLATE_DEBUG = DEBUG

"""
TIME_ZONE

Sets the used time zone.

Default: 'America/Chicago'
"""
#TIME_ZONE = 'America/Chicago'

"""
LANGUAGE_CODE

Sets the language code.

Default: 'en-us'
"""
#LANGUAGE_CODE = 'en-us'

"""
ADMINS

A list of chaps maintaining the app.

Default: ()
"""
ADMINS = (
     ('John Doe', 'john.doe@example.org'),
)

STATICFILES_DIRS += (
    os.path.join(PROJECT_DIR, 'static'),
)

"""
DATABASES

Database-stuff.

Default: SQLite database
"""
#DATABASES = {
# 'default': {
# # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3'.
# 'ENGINE': 'django.db.backends.sqlite3',
# # Or path to database file if using sqlite3.
# 'NAME': PROJECT_DIR + '/teerace.sqlite',
# # Not used with sqlite3.
# 'USER': '',
# # Not used with sqlite3.
# 'PASSWORD': '',
# # Set to empty string for localhost. Not used with sqlite3.
# 'HOST': '',
# # Set to empty string for default. Not used with sqlite3.
# 'PORT': '',
# }
#}

"""
MIDDLEWARE_CLASSES

You might want to add some debug stuff here.
"""
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

"""
INSTALLED_APPS

You might want to add some debug stuff here.
"""
INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
    'kombu.transport.django',  # needed because the django databse is used as celery broker
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}

INTERNAL_IPS = ('127.0.0.1')

# Broker URL for celery. Using the django databse here
BROKER_URL = 'django://'

# Email settings
EMAIL_HOST = 'smtp.example.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'johndoeuptee'
EMAIL_HOST_PASSWORD = 'example'
EMAIL_USE_TLS = False
SERVER_EMAIL = 'johndoeuptee@example.org'
EMAIL_SUBJECT_PREFIX = '[upTee]: '

# server executable
SERVER_EXEC = 'teeworlds_srv'

PYBROWSCAP_INITIALIZE = True
