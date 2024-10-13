from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


from projects.tasks.fetch_favicon import fetch_favicon

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# monitor/celery.py
app = Celery('src')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'refresh_favicon': {
        'task': 'projects.tasks.refresh_favicon.refresh_favicon',
        'schedule': 4.0,  # Run every 4 seconds
    },
}