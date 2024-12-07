import logging
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from performances.models import Lighthouse
from .tasks.fetch_favicon import fetch_favicon
from .tasks.fetch_sitemap import fetch_sitemap
from .tasks.scrape_page import scrape_page
from .models import Project, Pages

DELAY_REFRESH_FAVICON_SECONDS = 30 # Every 30 seconds

@receiver(post_save, sender=Project)
def post_save_created(sender, instance, created, **kwargs):

    if created:
        instance.favicon_task_status = 'PENDING'
        instance.favicon_last_edited = timezone.now()
        instance.save()
        fetch_sitemap.delay(instance.pk, instance.url)
        fetch_favicon.delay(instance.pk, instance.url)

@receiver(post_save, sender=Pages)
def post_save_created_page(sender, instance, created, **kwargs):

    if created:
        # Fetch title and description
        scrape_page.delay(instance.pk, instance.url)
        # Create Performance model
        Lighthouse.objects.create(page=instance)
