from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    """
    A user own a project he want to monitor and work on.
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "applications",
    )
    title = models.CharField(max_length=128, blank=False)

    def is_online(self):
        return not self.services.filter(instancedownincidents__status=2)

    def is_offline(self):
        return self.services.filter(instancedownincidents__status=2, is_critical=True, is_enabled=True)

    def is_degraded(self):
        return self.services.filter(instancedownincidents__status=2, is_critical=False, is_enabled=True)

    def availability(self, days=30):

        from incidents.models import InstanceDownIncident

        total_second = days * 24 * 60 * 60
        start_date = timezone.now() - timezone.timedelta(days=days)

        alerts = InstanceDownIncident.objects.filter(service__in=self.services.filter(is_critical=True), severity=2, endsAt__gte=start_date) | InstanceDownIncident.objects.filter(service__in=self.services.filter(is_critical=True), severity=2, endsAt__isnull=True)

        total_unavailability = 0
        for alert in alerts:
            if not alert.endsAt:
                total_unavailability += (timezone.now() - alert.startsAt).seconds
            elif alert.startsAt < start_date:
                total_unavailability += (alert.endsAt - start_date).seconds
            else:
                total_unavailability += alert.duration.seconds

        return round(100 - total_unavailability * 100 / total_second, 3)

    def __str__(self):
        return self.title

class Service(models.Model):
    """
    Each project run a list of services which will be monitor by the application.
    A service can be a URL http code
    """
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "services",
    )
    title = models.CharField(max_length=128, blank=False)
    is_public = models.BooleanField('Is visible', default=True, help_text="Service will appears on application status board")
    is_enabled = models.BooleanField(default=True, help_text="Disabled service will not be monitored")
    is_critical = models.BooleanField(default=True, help_text="Application is offline if this service fail, otherwise will only report as degraded")
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")

    def availability(self, days=30):

        from incidents.models import InstanceDownIncident

        total_second = days * 24 * 60 * 60
        start_date = timezone.now() - timezone.timedelta(days=days)

        alerts = InstanceDownIncident.objects.filter(service=self, severity=2, endsAt__gte=start_date) | InstanceDownIncident.objects.filter(service=self, severity=2, endsAt__isnull=True)

        total_unavailability = 0
        for alert in alerts:
            if not alert.endsAt:
                total_unavailability += (timezone.now() - alert.startsAt).seconds
            elif alert.startsAt < start_date:
                total_unavailability += (alert.endsAt - start_date).seconds
            else:
                total_unavailability += alert.duration.seconds

        return round(100 - total_unavailability * 100 / total_second, 3)

    def is_online(self):
        return not self.instancedownincidents.filter(endsAt__isnull=True)

    def is_offline(self):
        return self.instancedownincidents.filter(status=2, endsAt__isnull=True)

    def is_degraded(self):
        return self.instancedownincidents.filter(status=2, endsAt__isnull=True)

    def __str__(self):
        return f'{self.project} - {self.title}'

class HTTPCodeService(models.Model):
    url = models.URLField(max_length=512, blank=False)
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE,
        related_name = "httpcode",
    )

HTTP_CODES = [
    (200, '200 - OK'),
    (404, '404 - Not Found'),
    (418, '418 - I’m a teapot'),
    (500, '500 - Internal Server Error'),
]

class HTTPMockedCodeService(models.Model):
    code = models.IntegerField(choices=HTTP_CODES)
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE,
        related_name = "httpmockedcode",
    )