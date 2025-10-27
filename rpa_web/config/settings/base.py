"""
Django base settings for RPA Web project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env.dev
# This makes them available to the Django application
dotenv_path = BASE_DIR / '.env.dev'
load_dotenv(dotenv_path=dotenv_path)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'django_summernote',

    # Local apps
    'rpa_bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'th'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Summernote Configuration
SUMMERNOTE_CONFIG = {
    'summernote': {
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
            ['mybutton', ['codeBlock']],  # Custom code block button
        ],
        'width': '100%',
        'height': '480',
        'codemirror': {
            'mode': 'python',
            'lineNumbers': True,
            'theme': 'monokai',
        },
        'codeviewFilter': False,
        'codeviewIframeFilter': True,
    },
    'attachment_filesize_limit': 1024 * 1024 * 10,  # 10MB
    'attachment_require_authentication': True,
    'disable_attachment': False,
    'lazy': True,
}

# X Frame Options for Summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'rpa_bot': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# RPA Bot Settings
RPA_SCREENSHOT_DIR = BASE_DIR / 'screenshots'
RPA_MAX_TASK_DURATION = 600  # 10 minutes in seconds
RPA_DEFAULT_DELAY = 3  # seconds
RPA_DEFAULT_MAX_RETRIES = 3


# Celery Configuration
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_TIMEZONE = 'Asia/Bangkok'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Celery Beat Schedule - Daily News Intelligence at 10:00 AM
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Task 1: Scrape ข่าวอัตโนมัติทุก 10 นาที ทุกวัน
    'hourly-scrape-news': {
        'task': 'rpa_bot.tasks.scrape_all_news',
        'schedule': crontab(minute='*/10'),  # ทุกๆ 10 นาที
        'options': {
            'expires': 600,  # Expire after 10 minutes if not executed
        }
    },
    # Task 2: สร้างรายงานทุก 10 นาที (หลัง scrape 3 นาที)
    'hourly-generate-report': {
        'task': 'rpa_bot.tasks.generate_daily_report',
        'schedule': crontab(minute='3-59/10'),  # นาทีที่ 3, 13, 23, 33, 43, 53
        'options': {
            'expires': 600,
        }
    },
    # Task 3: ส่งรายงานไปยัง Telegram ทุก 10 นาที (หลัง generate 2 นาที)
    'hourly-send-telegram-report': {
        'task': 'rpa_bot.tasks.send_daily_report',
        'schedule': crontab(minute='5-59/10'),  # นาทีที่ 5, 15, 25, 35, 45, 55
        'options': {
            'expires': 600,
        }
    },
    # Weekly cleanup
    'cleanup-old-articles-weekly': {
        'task': 'rpa_bot.tasks.cleanup_old_articles',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # ทุกวันอาทิตย์ เวลา 02:00 น.
        'kwargs': {'days': 30}
    },
}
