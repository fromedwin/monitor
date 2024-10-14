from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# monitor/celery.py
app = Celery('src')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'refresh_favicon': {
        'task': 'projects.tasks.refresh_favicon.refresh_favicon',
        'schedule': 60.0,  # Run every 60 seconds
    },
}