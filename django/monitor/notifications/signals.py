from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Pager_Duty
from clients.config import generate_alert_manager_config
from projects.models import Project

@receiver(post_save, sender=Pager_Duty)
@receiver(post_delete, sender=Pager_Duty)
@receiver(post_delete, sender=Project)
def refresh_alert_manager_configuration(sender, instance=None, created=False, **kwargs):
    """
    Assign a django rest framework token when a user is created.
    """
    generate_alert_manager_config()