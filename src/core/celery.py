from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# monitor/celery.py
app = Celery('src')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'queue_deprecated_favicons': {
        'task': 'projects.tasks.queue_deprecated_favicons.queue_deprecated_favicons',
        'schedule': 360,  # Run every 60 seconds
    },
    'queue_deprecated_sitemaps': {
        'task': 'projects.tasks.queue_deprecated_sitemaps.queue_deprecated_sitemaps',
        'schedule': 360, #24 * 60 * 60,  # Run every 24 hours
    },
    'queue_deprecated_performance': {
        'task': 'performances.tasks.queue_deprecated_performance.queue_deprecated_performance',
        'schedule': 30, #24 * 60 * 60,  # Run every 24 hours
    },
}