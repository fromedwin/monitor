from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Alerts, Metrics, Server
from projects.models import Project
from availability.models import Service
from django.utils import timezone
from notifications.models import Pager_Duty

@receiver(post_save, sender=Alerts)
@receiver(post_delete, sender=Alerts)
@receiver(post_delete, sender=Project)
@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
@receiver(post_save, sender=Metrics)
@receiver(post_delete, sender=Metrics)
@receiver(post_save, sender=Pager_Duty)
@receiver(post_delete, sender=Pager_Duty)
def update_last_modified_setup(sender, instance=None, created=False, **kwargs):
    """
    Refresh server last_modified_setup date when modifying Alerts, Project, Service, Metrics
    """
    servers = Server.objects.all()
    for server in servers:
        server.last_modified_setup = timezone.now()
        server.save()
