from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lighthouse
from celery import current_app

DELAY_REFRESH_FAVICON_SECONDS = 30 # Every 30 seconds

@receiver(post_save, sender=Lighthouse)
def post_save_created(sender, instance, created, **kwargs):

    if created:
        instance.last_request_date = timezone.now()
        instance.save()
        task_kwargs = {'id': instance.pk, 'url': instance.url}
        current_app.send_task('fetch_lighthouse_report', kwargs=task_kwargs, queue=settings.CELERY_QUEUE_LIGHTHOUSE, task_id=f'performance_{instance.pk}')