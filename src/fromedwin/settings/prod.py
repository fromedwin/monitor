"""
Production settings for fromedwin project.
"""

from .base import *
from .timings import PRODUCTION;

# Override debug mode for production
DEBUG = False

# Production security settings
SECURE_SSL_REDIRECT = FORCE_HTTPS
SECURE_HSTS_SECONDS = 31536000 if FORCE_HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = FORCE_HTTPS
SECURE_HSTS_PRELOAD = FORCE_HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Production-specific database configuration
# Use environment variable DATABASE_URL for production
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in production")

# Production email settings
if not EMAIL_HOST:
    raise ValueError("EMAIL_HOST must be set in production")

# Production static files (remove django_browser_reload middleware)
MIDDLEWARE = tuple([
    item for item in MIDDLEWARE 
    if item != 'django_browser_reload.middleware.BrowserReloadMiddleware'
])

# Remove django_browser_reload from installed apps
INSTALLED_APPS = [
    app for app in INSTALLED_APPS 
    if app != 'django_browser_reload'
]

# Production logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'fromedwin': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Production caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}

TIMINGS = PRODUCTION;

# Production session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Production performance settings
CELERY_TASK_ALWAYS_EAGER = False  # Use actual task queue in production 