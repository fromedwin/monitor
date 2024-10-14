from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .tasks.fetch_favicon import fetch_favicon
from .models import Project

DELAY_REFRESH_FAVICON_SECONDS = 10 # Every 10 seconds

@receiver(pre_save, sender=Project)
def post_save_fetch_favicon(sender, instance=None, **kwargs):
    favicon_need_refresh = False

    # Fetch the existing instance from the database if it exists
    if instance.pk:
        try:
            old_instance = Project.objects.get(pk=instance.pk)
            # Check if the favicon value has changed
            if old_instance.favicon != instance.favicon:
                instance.favicon_task_status = 'SUCCESS'
                instance.favicon_last_edited = timezone.now()
        except Project.DoesNotExist:
            # If the object does not exist in the database, it's a new object
            favicon_need_refresh = True
    else:
        # If instance.pk is None, it's a new object
        favicon_need_refresh = True

    if instance.favicon_task_status == 'UNKNOWN':
        favicon_need_refresh = True
    if (timezone.now() - instance.favicon_last_edited).seconds > DELAY_REFRESH_FAVICON_SECONDS and instance.favicon_task_status != 'PENDING':
        favicon_need_refresh = True

    if favicon_need_refresh:
        instance.favicon_task_status = 'PENDING'
        fetch_favicon.delay(instance.pk, instance.url)