# start_celery_beat.py
import os
from subprocess import call
from dotenv import load_dotenv

load_dotenv()

beat_hostname = os.getenv('CELERY_BEAT_HOSTNAME', 'default_beat_name')

# Start Celery Beat using the hostname defined
call([
    'celery', '-A', 'core', 'beat',
    '--loglevel=info',
    '--scheduler', 'django_celery_beat.schedulers:DatabaseScheduler',
])