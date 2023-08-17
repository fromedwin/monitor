from django.db import models

from projects.models import Project
from constants import INCIDENT_SEVERITY_CHOICES

class Alerts(models.Model):
    """
        
    """
    name = models.CharField(max_length=128, help_text="Alert name", unique=True)
    is_critical = models.BooleanField(default=False, help_text="Trigger an outrage when critical alert is triggered")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

class AlertsWarning(models.Model):
    """
        
    """
    alert = models.OneToOneField(
        Alerts,
        on_delete = models.CASCADE,
        related_name = "warning",
        unique = True,
    )
    expr = models.CharField(max_length=128)
    duration = models.CharField(max_length=8, default='2m')
    summary = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.alert.name

    class Meta:
        verbose_name = "Warning"
        verbose_name_plural = "Warnings"

class AlertsCritical(models.Model):
    """
        
    """
    alert = models.OneToOneField(
        Alerts,
        on_delete = models.CASCADE,
        related_name = "critical",
        unique = True,
    )
    expr = models.CharField(max_length=128)
    duration = models.CharField(max_length=8, default='5m')
    summary = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.alert.name

    class Meta:
        verbose_name = "Critical"
        verbose_name_plural = "Criticals"

class DisableAlerts(models.Model):
    """
        Specify disabled alerts
    """
    alert = models.ForeignKey(
        Alerts,
        on_delete = models.CASCADE,
        related_name = "disable_alert",
    )
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "disable_alerts",
    )

    class Meta:
        verbose_name = "Disable Alert"
        verbose_name_plural = "Disable Alerts"
