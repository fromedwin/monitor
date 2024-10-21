from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks.fetch_favicon import fetch_favicon
from .tasks.fetch_sitemap import fetch_sitemap
from .models import Project

DELAY_REFRESH_FAVICON_SECONDS = 30 # Every 30 seconds

@receiver(post_save, sender=Project)
def post_save_created(sender, instance, created, **kwargs):

    if created:
        instance.favicon_task_status = 'PENDING'
        instance.favicon_last_edited = timezone.now()
        fetch_sitemap.delay(instance.pk, instance.url)
        fetch_favicon.delay(instance.pk, instance.url)