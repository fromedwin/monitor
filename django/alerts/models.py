from django.db import models

from constants import INCIDENT_SEVERITY_CHOICES

class Alerts(models.Model):
    """
        This model is straight export from prometheus alertmanager spec description
    """
    alert = models.CharField(max_length=128)
    expr = models.CharField(max_length=128)
    duration = models.CharField(max_length=8)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY_CHOICES)
    summary = models.TextField()
    description = models.TextField()
