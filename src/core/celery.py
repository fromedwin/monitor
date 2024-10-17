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
        'schedule': 60.0,  # Run every 60 seconds
    },
}