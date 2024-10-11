# start_celery_beat.py
import os
from subprocess import call

beat_hostname = os.getenv('CELERY_WORKER_HOSTNAME', 'fromedwin.worker')

# Start Celery Beat using the hostname defined
call([
    'celery', '-A', 'core', 'worker',
    '--loglevel=info',
    f'--hostname={beat_hostname}',
])