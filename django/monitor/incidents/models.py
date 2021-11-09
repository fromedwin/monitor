from django.db import models
from django.contrib.auth.models import User
from projects.models import Project, Service 
from django.template.defaultfilters import truncatechars
from django.utils import timezone

INCIDENT_STATUS = [
    (0, 'unknown'),
    (1, 'resolved'),
    (2, 'firing'),
]

INCIDENT_SEVERITY = [
    (0, 'unknown'),
    (1, 'warning'),
    (2, 'critical'),
]

class AbstractIncident(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    json = models.TextField(blank=False, help_text="RAW json as received by the webhook")
    fingerprint = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        editable=False,
        help_text="Fingerprint provided by prometheus"
    )

    class Meta:
        abstract = True

    @property
    def short_json(self):
        return "%s..." % truncatechars(self.json, 70)

class GenericIncident(AbstractIncident):

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "genericincidents",
        blank = True,
        null = True,
    )

    status = models.IntegerField(choices=INCIDENT_STATUS)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY)

    startsAt = models.DateTimeField(null=False)
    endsAt = models.DateTimeField(null=True, blank=True)

    instance = models.TextField(null=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)

    @property
    def duration(self):
        if self.endsAt:
            return  self.endsAt - self.startsAt
        return timezone.now() - self.startsAt
    
    class Meta:
        verbose_name = "Unknown alert"
        verbose_name_plural = "Unknown alerts"

class ProjectIncident(AbstractIncident):

    project = models.ForeignKey(
        Project,
        null=True,
        on_delete = models.CASCADE,
        related_name = "projectincident",
    )

    status = models.IntegerField(choices=INCIDENT_STATUS)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY)

    startsAt = models.DateTimeField(null=False)
    endsAt = models.DateTimeField(null=True, blank=True)

    instance = models.TextField(null=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)

    @property
    def duration(self):
        if self.endsAt:
            return  self.endsAt - self.startsAt
        return timezone.now() - self.startsAt

    class Meta:
        verbose_name = "Project alert"
        verbose_name_plural = "Project alerts"

class InstanceDownIncident(AbstractIncident):

    service = models.ForeignKey(
        Service,
        null=True,
        on_delete = models.CASCADE,
        related_name = "instancedownincidents",
    )

    status = models.IntegerField(choices=INCIDENT_STATUS)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY)

    startsAt = models.DateTimeField(null=False)
    endsAt = models.DateTimeField(null=True, blank=True)

    instance = models.TextField(null=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)

    @property
    def duration(self):
        if self.endsAt:
            return  self.endsAt - self.startsAt
        return timezone.now() - self.startsAt

    class Meta:
        verbose_name = "Service down incident"
        verbose_name_plural = "Service down incidents"
