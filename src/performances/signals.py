from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Performance
from celery import current_app

DELAY_REFRESH_FAVICON_SECONDS = 30 # Every 30 seconds
QUEUE_NAME = 'fromedwin_lighthouse_queue'

@receiver(post_save, sender=Performance)
def post_save_created(sender, instance, created, **kwargs):

    if created:
        instance.last_request_date = timezone.now()
        instance.save()
        task_kwargs = {'id': instance.pk, 'url': instance.url}
        current_app.send_task('fetch_lighthouse_report', kwargs=task_kwargs, queue=QUEUE_NAME, task_id=f'performance_{instance.pk}')