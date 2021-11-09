from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from projects.models import Application
from clients.config import generate_alert_manager_config
# Create your models here.

class Pager_Duty(models.Model):
    """
    Assign a pager duty API token to an application
    """
    application = models.ForeignKey(
        Application,
        on_delete = models.CASCADE,
        related_name = "pager_duty",
        blank=False,
    )
    routing_key = models.CharField(max_length=32, blank=False)

    class Meta:
        verbose_name = "Pager Duty key"
        verbose_name_plural = "Pager Duty keys"

@receiver(post_save, sender=Pager_Duty)
@receiver(post_delete, sender=Pager_Duty)
@receiver(post_delete, sender=Application)
def refresh_alert_manager_configuration(sender, instance=None, created=False, **kwargs):
    """
    Assign a django rest framework token when a user is created.
    """
    generate_alert_manager_config()