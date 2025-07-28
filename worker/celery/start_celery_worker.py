# start_celery_worker.py
import os
from subprocess import call
from dotenv import load_dotenv

load_dotenv()

worker_hostname = os.getenv('CELERY_WORKER_HOSTNAME', 'fromedwin.worker')

# Start Celery Worker with concurrency=1 to process tasks one by one
call([
    'celery', '-A', 'fromedwin', 'worker',
    '--loglevel=info',
    f'--hostname={worker_hostname}',
    '--concurrency=1',  # Process only one task at a time
])