"""
Django settings for newsportal project.

Generated by 'set DJANGO_SETTINGS_MODULE=<путь к файлу настроек>.settings startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from config import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k#e&i=fq7o95xk_910=q^jjk5eg&x)s&)w&*xz1f!absf@xiy='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['http://127.0.0.1:8000/']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'fpages',
    'app',
    'django_filters',
    'allauth',
    'allauth.account',
    'django_apscheduler',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'newsportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
WSGI_APPLICATION = 'newsportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_REDIRECT_URL = '/news/'  # Redirect to homepage after login
LOGOUT_REDIRECT_URL = '/login/'  # Redirect to login page after logout
LOGIN_URL = '/accounts/login/'

# Email login functionality
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'signup': 'app.forms.BasicSignupForm'}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

APSCHEDULER_RUN_NOW_TIMEOUT = 25    # If task is not completed in this number of seconds it will be cancelled


CELERY_BROKER_URL = \
    'redis://:YeO79TVHe5vXcKQSOF843HQpwt9x0mDd@redis-17183.c281.us-east-1-2.ec2.redns.redis-cloud.com:17183/0'
CELERY_RESULT_BACKEND = \
    'redis://:YeO79TVHe5vXcKQSOF843HQpwt9x0mDd@redis-17183.c281.us-east-1-2.ec2.redns.redis-cloud.com:17183/0'

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


CELERY_BEAT_SCHEDULE = {
    'send_every_monday_8am': {
        'task': 'app.tasks.send_weekly_newsletter',
        'schedule': crontab(day_of_week='monday', hour='8', minute='0'),  # Every Monday at 8 AM
    },
    'debug-task': {
        'task': 'app.tasks.debug_task',
        'schedule': crontab(minute='*/1'),  # Every minute
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s '
                      '%(levelname)s '
                      '%(message)s'
        },
        'detailed': {
            'format': '%(asctime)s '
                      '%(levelname)s '
                      '%(pathname)s '
                      '%(module)s '
                      '%(message)s'
        },

        'error_critical': {
            'format': '%(asctime)s '
                      '%(levelname)s '
                      '%(pathname)s '
                      '%(message)s '
                      '%(exc_info)s'
        },
        'error_email': {
            'format': '%(asctime)s '
                      '%(levelname)s '
                      '%(pathname)s '
                      '%(message)s '
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },

        'require_debug_false': {
            '()': 'app.log_filters.RequireDebugFalse',  # Add the custom filter from log_filters.py
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',   # Send log messages to the console
            'formatter': 'simple'
        },
        'console_warning': {
            'filters': ['require_debug_true'],
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        },

        'console_error': {
            'filters': ['require_debug_true'],
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'error_critical'
        },

        'file_general': {
            'filters': ['require_debug_false'],
            'level': 'INFO',
            'class': 'logging.FileHandler',     # Send log messages to a file
            'filename': 'general.log',
            'formatter': 'detailed'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',     # Send log messages to a file
            'filename': 'errors.log',
            'formatter': 'error_critical'
        },

        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',     # Send log messages to a file
            'filename': 'security.log',
            'formatter': 'detailed'
        },

        'mail_admins': {
            'filters': ['require_debug_false'],
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',  # Send error logs via email to the site admins
            'formatter': 'error_email'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_warning', 'console_error', 'file_general'],  # Added file handler
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file_general', 'file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['mail_admins', 'file_general', 'file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_general', 'file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_general', 'file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

