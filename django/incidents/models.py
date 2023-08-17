import humanize

from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from availability.models import Service 
from django.template.defaultfilters import truncatechars
from django.utils import timezone

from alerts.models import Alerts
from projects.models import Project

from constants import INCIDENT_STATUS_CHOICES, INCIDENT_SEVERITY_CHOICES

class Incident(models.Model):
    """
        Based on AlertManager model, an incident is received from alertmanager
        user the `webhook` function from `view.py`.
    """
    starts_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(choices=INCIDENT_STATUS_CHOICES)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY_CHOICES)

    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    json = models.TextField(blank=False, help_text="RAW json as received by the webhook")

    @property
    def duration(self):
        if self.endsAt:
            return  self.endsAt - self.startsAt
        return timezone.now() - self.startsAt

    @property
    def short_json(self):
        return "%s..." % truncatechars(self.json, 70)

    @property
    def message(self):
        return self.description

class ServiceIncident(models.Model):

    incident = models.OneToOneField(
        Incident,
        on_delete = models.CASCADE,
        related_name = "service_incidents",
        unique = True,
    )
    service = models.ForeignKey(
        Service,
        null = False,
        on_delete = models.CASCADE,
        related_name = "incidents",
    )
    alert = models.ForeignKey(
        Alerts,
        null = False,
        on_delete = models.CASCADE,
        related_name = "service_incidents",
    )

class UnknownIncident(models.Model):

    incident = models.OneToOneField(
        Incident,
        on_delete = models.CASCADE,
        related_name = "unknown_incidents",
        unique = True,
    )
    alert_name = models.CharField(max_length=128, help_text="Alert name", unique=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)
