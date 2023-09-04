import humanize

from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from availability.models import Service 
from django.template.defaultfilters import truncatechars
from django.utils import timezone

from projects.models import Project

from constants import INCIDENT_STATUS_CHOICES, INCIDENT_SEVERITY_CHOICES, INCIDENT_SEVERITY

class Incident(models.Model):
    """
        Based on AlertManager model, an incident is received from alertmanager
        user the `webhook` function from `view.py`.
    """
    alert_name = models.CharField(max_length=128, help_text="Alert name")

    starts_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(choices=INCIDENT_STATUS_CHOICES)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY_CHOICES)

    summary = models.TextField(null=True)
    description = models.TextField(null=True)

    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    json = models.TextField(blank=False, help_text="RAW json as received by the webhook")

    service = models.ForeignKey(
        Service,
        null = True,
        on_delete = models.CASCADE,
        related_name = "incidents",
    )

    @property
    def duration(self):
        if self.ends_at:
            return  self.ends_at - self.starts_at
        return timezone.now() - self.starts_at

    @property
    def short_json(self):
        return "%s..." % truncatechars(self.json, 70)

    @property
    def is_critical(self):
        return self.severity == INCIDENT_SEVERITY['CRITICAL']
