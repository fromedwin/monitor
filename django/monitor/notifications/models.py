from django.db import models
from applications.models import Application
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