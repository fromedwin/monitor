from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromedwin.settings.prod')

# monitor/celery.py
app = Celery('src')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Celery settings
app.conf.update({
    'task_default_queue': settings.CELERY_QUEUE,
    'worker_prefetch_multiplier': 1,
})
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'queue_deprecated_favicons': {
        'task': 'favicons.tasks.queue_deprecated_favicons',
        'schedule': 60,  # Run every 60 seconds
    },
    'queue_deprecated_sitemaps': {
        'task': 'projects.tasks.queue_deprecated_sitemaps.queue_deprecated_sitemaps',
        'schedule': 60, #24 * 60 * 60,  # Run every 24 hours
    },
    'queue_deprecated_performance': {
        'task': 'lighthouse.tasks.queue_deprecated_performance.queue_deprecated_performance',
        'schedule': 30, #24 * 60 * 60,  # Run every 24 hours
    },
    'queue_report_creation': {
        'task': 'reports.tasks.queue_report_creation.queue_report_creation',
        'schedule': 60,  # Run every 60 seconds
    },
}