from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lighthouse
from celery import current_app

@receiver(post_save, sender=Lighthouse)
def post_save_created(sender, instance, created, **kwargs):

    if created:
        instance.last_request_date = timezone.now()
        instance.save()
