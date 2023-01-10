from django.db import models
from django.contrib.auth.models import User
from projects.models import Project, Service 
from django.template.defaultfilters import truncatechars
from django.utils import timezone

STATUS_UNKNOWN = 0
STATUS_RESOLVED = 1
STATUS_FIRING = 2

SEVERITY_UNKNOWN = 0
SEVERITY_WARNING = 1
SEVERITY_CRITICAL = 2

INCIDENT_STATUS = [
    (STATUS_UNKNOWN, 'unknown'),
    (STATUS_RESOLVED, 'resolved'),
    (STATUS_FIRING, 'firing'),
]

INCIDENT_SEVERITY = [
    (SEVERITY_UNKNOWN, 'unknown'),
    (SEVERITY_WARNING, 'warning'),
    (SEVERITY_CRITICAL, 'critical'),
]

class AbstractIncident(models.Model):
    """
        Dased on AlertManager model, an incident is received from alertmanager
        user the `webhook` function from `view.py`.
    """

    instance = models.TextField(null=True)
    summary = models.TextField(null=True)
    description = models.TextField(null=True)

    startsAt = models.DateTimeField(null=False)
    endsAt = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(choices=INCIDENT_STATUS)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY)

    # alerts have a unique identifier
    fingerprint = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        editable=False,
        help_text="Fingerprint provided by prometheus"
    )
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    json = models.TextField(blank=False, help_text="RAW json as received by the webhook")

    class Meta:
        abstract = True

    @property
    def duration(self):
        if self.endsAt:
            return  self.endsAt - self.startsAt
        return timezone.now() - self.startsAt

    @property
    def short_json(self):
        return "%s..." % truncatechars(self.json, 70)

class InstanceDownIncident(AbstractIncident):
    """
        This incident is trigger when a non HTTP_Code 200 is detected on
        service url.
    """
    service = models.ForeignKey(
        Service,
        null=True,
        on_delete = models.CASCADE,
        related_name = "instancedownincidents",
    )

    class Meta:
        verbose_name = "Service down incident"
        verbose_name_plural = "Service down incidents"
    
class ProjectIncident(AbstractIncident):
    """
        If an Incident has a project id assigned to it, we separate it from GenericIncident
        as it is assigned from a specific project.
    """
    project = models.ForeignKey(
        Project,
        null=True,
        on_delete = models.CASCADE,
        related_name = "projectincident",
    )

    class Meta:
        verbose_name = "Project alert"
        verbose_name_plural = "Project alerts"

class GenericIncident(AbstractIncident):
    """
        This is a default incident, could be a server node_exporter alert
        or a django one. It could be assigned to a user, or if not displayed
        to all admins.
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "genericincidents",
        blank = True,
        null = True,
    )
    
    class Meta:
        verbose_name = "Unknown alert"
        verbose_name_plural = "Unknown alerts"
