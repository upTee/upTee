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
#DEBUG = True

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
TIME_ZONE = 'America/Chicago'

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

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

"""
DATABASES

Database-stuff.

Default: SQLite database
"""
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': 'uptee',
        # Not used with sqlite3.
        'USER': 'john',
        # Not used with sqlite3.
        'PASSWORD': 'examplepass',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

EMAIL_HOST = 'smtp.example.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'johndoeuptee'
EMAIL_HOST_PASSWORD = 'example'
EMAIL_USE_TLS = False
SERVER_EMAIL = 'johndoeuptee@example.org'
EMAIL_SUBJECT_PREFIX = '[upTee]: '

#SERVER_EXEC = 'teeworlds_srv'

SECRET_KEY = 'k3z^qa7!j7#u3^+^^3)e(eo3^_@gmyml2+412w1qp0^r+d^c6p'  # Change thisto something secret!

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
)

CACHES = {
    'default': dict(
        BACKEND='johnny.backends.memcached.MemcachedCache',
        LOCATION=['127.0.0.1:11211'],
        JOHNNY_CACHE=True,
    )
}
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_uptee'

TEMPLATE_CACHING = True

if TEMPLATE_CACHING:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

CELERYD_LOG_FILE = "/var/log/celery.log"

#ANALYTICS_ID = '' # add the analytics id here

PYBROWSCAP_UPDATE = False

if DEBUG:
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
