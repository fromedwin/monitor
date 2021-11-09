from django.db import models
from django.contrib.auth.models import User
from projects.models import Service, Application
from django.template.defaultfilters import truncatechars
from django.utils import timezone

class AbstractAlert(models.Model):
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

class GenericAlert(AbstractAlert):

    STATUS = [
        (0, 'unknown'),
        (1, 'resolved'),
        (2, 'firing'),
    ]

    SEVERITY = [
        (0, 'unknown'),
        (1, 'warning'),
        (2, 'critical'),
    ]

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "genericalerts",
        blank = True,
        null = True,
    )

    status = models.IntegerField(choices=STATUS)
    severity = models.IntegerField(choices=SEVERITY)

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

class ApplicationAlert(AbstractAlert):

    STATUS = [
        (0, 'unknown'),
        (1, 'resolved'),
        (2, 'firing'),
    ]

    SEVERITY = [
        (0, 'unknown'),
        (1, 'warning'),
        (2, 'critical'),
    ]

    application = models.ForeignKey(
        Application,
        null=True,
        on_delete = models.CASCADE,
        related_name = "applicationalerts",
    )

    status = models.IntegerField(choices=STATUS)
    severity = models.IntegerField(choices=SEVERITY)

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
        verbose_name = "Application alert"
        verbose_name_plural = "Application alerts"


# Create your models here.
class InstanceDownAlert(AbstractAlert):

    STATUS = [
        (0, 'unknown'),
        (1, 'resolved'),
        (2, 'firing'),
    ]

    SEVERITY = [
        (0, 'unknown'),
        (1, 'warning'),
        (2, 'critical'),
    ]

    service = models.ForeignKey(
        Service,
        null=True,
        on_delete = models.CASCADE,
        related_name = "instancedownalerts",
    )

    status = models.IntegerField(choices=STATUS)
    severity = models.IntegerField(choices=SEVERITY)

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
        verbose_name = "Service down alert"
        verbose_name_plural = "Service down alerts"

