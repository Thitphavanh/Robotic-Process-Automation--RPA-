"""
Development settings for RPA Web project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dev-key-change-in-production-12345'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Development-specific apps
INSTALLED_APPS += [
    # 'debug_toolbar',  # Uncomment if you want Django Debug Toolbar
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # Uncomment with Debug Toolbar
]


# Debug Toolbar settings (if enabled)
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]


# Email Backend for Development (Console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Logging - More verbose in development
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['rpa_bot']['level'] = 'DEBUG'


# CORS settings for development (if using CORS)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# Development-specific settings
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False


# Cache - Simple cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


# RPA Settings for Development
RPA_SCREENSHOT_DIR = BASE_DIR / 'screenshots'
RPA_DEFAULT_DELAY = 5  # Longer delay for development/testing
