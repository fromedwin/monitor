from django.db import models

from projects.models import Project

class Pager_Duty(models.Model):
    """
    Assign a pager duty API token to an application
    """
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "pager_duty",
        blank=False,
        unique=True
    )
    routing_key = models.CharField(max_length=32, blank=False)

    class Meta:
        verbose_name = "Pager Duty key"
        verbose_name_plural = "Pager Duty keys"
