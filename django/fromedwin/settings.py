"""
Django settings for fromedwin project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
DOMAIN = os.environ.get('DOMAIN')
PORT = os.environ.get('PORT')
WEBAUTH_USERNAME = os.environ.get('WEBAUTH_USERNAME')
WEBAUTH_PASSWORD = os.environ.get('WEBAUTH_PASSWORD')

IS_SERVICE_DOWN_SCRAPE_INTERVAL = '1m'
IS_SERVICE_DOWN_TRIGGER_OUTRAGE_MINUTES = 5

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    'host.docker.internal',
    'status.fromedwin.com',
    os.environ.get('DOMAIN'),
]

MIDDLEWARE = ()

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

if os.environ.get('STORAGE') == 'whitenoise':
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    MIDDLEWARE = MIDDLEWARE + ('whitenoise.middleware.WhiteNoiseMiddleware',)


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Application definition

# TAILWIND SETTINGS
TAILWIND_APP_NAME = 'theme' # Tailwind theme
INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    # Tailwind
    'theme',
    'tailwind',
    'django_browser_reload',
    # App
    'administration',
    'dashboard',
    'incidents',
    'fromedwin',
    'notifications',
    'settings',
    'projects',
    'website',
    'workers',
    # Statistics
    'django_prometheus',
]

MIDDLEWARE = (
    'django_prometheus.middleware.PrometheusAfterMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
    'fromedwin.middleware.is_allowed_user',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
)

ROOT_URLCONF = 'fromedwin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fromedwin.wsgi.application'

# Database confugration using environment variable DATABASES_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {}
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
        ],
    }
}

HEARTBEAT_INTERVAL = 10 # client will call server every HEARTBEAT_INTERVAL seconds.

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
