# start_celery_worker.py
import os
from subprocess import call
from dotenv import load_dotenv

load_dotenv()

worker_hostname = os.getenv('CELERY_WORKER_HOSTNAME', 'fromedwin.worker')

# Start Celery Worker using the hostname defined
call([
    'celery', '-A', 'fromedwin', 'worker',
    '--loglevel=info',
    f'--hostname={worker_hostname}',
])