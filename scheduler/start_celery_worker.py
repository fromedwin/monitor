# start_celery_worker.py
import os
from subprocess import call

worker_hostname = os.getenv('CELERY_WORKER_HOSTNAME', 'fromedwin.worker')

# Start Celery Worker using the hostname defined
call([
    'celery', '-A', 'core', 'worker',
    '--loglevel=info',
    f'--hostname={worker_hostname}',
])