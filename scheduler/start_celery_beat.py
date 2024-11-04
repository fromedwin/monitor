# start_celery_beat.py
import os
from subprocess import call
from dotenv import load_dotenv

load_dotenv()

beat_hostname = os.getenv('CELERY_BEAT_HOSTNAME', 'default_beat_name')

# If CELERY_BROKER user is not define we set default value
if not os.getenv('CELERY_BROKER_URL'):
    os.environ['CELERY_BROKER_URL'] = 'amqp://admin:admin@localhost'

# Start Celery Beat using the hostname defined
try:
    call([
        'celery', '-A', 'core', 'beat',
        '--loglevel=info',
        '--scheduler', 'django_celery_beat.schedulers:DatabaseScheduler',
        '--hostname', beat_hostname,
    ])
except Exception as e:
    print(f"Failed to start Celery Beat: {e}")