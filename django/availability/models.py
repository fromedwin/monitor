from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from projects.models import Project

from core.utils import is_private_ipv4

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

        from incidents.models import ServiceIncident

        total_second = days * 24 * 60 * 60
        start_date = timezone.now() - timezone.timedelta(days=days)

        alerts = ServiceIncident.objects.filter(service=self, incident__severity=2, incident__ends_at__gte=start_date) | ServiceIncident.objects.filter(service=self, incident__severity=2, incident__ends_at__isnull=True)

        total_unavailability = 0
        for alert in alerts:
            if not alert.incident.ends_at:
                total_unavailability += (timezone.now() - alert.incident.starts_at).seconds
            elif alert.incident.starts_at < start_date:
                total_unavailability += (alert.incident.ends_at - start_date).seconds
            else:
                total_unavailability += alert.incident.duration.seconds

        return round(100 - total_unavailability * 100 / total_second, 3)

    @property
    def is_offline(self):
        return self.incidents.filter(incident__status=2, incident__ends_at__isnull=True, incident__severity=2)

    @property
    def is_degraded(self):
        return self.incidents.filter(incident__status=2, incident__ends_at__isnull=True, incident__severity=2)

    @property
    def is_warning(self):
        if not self.is_critical:
            return False
        return self.incidents.filter(incident__status=2, incident__ends_at__isnull=True, incident__severity=1)

    def is_disabled(self):
        return not self.is_enabled

    def incidents_count(self):
        from incidents.models import ServiceIncident
        return ServiceIncident.objects.filter(service__in=self.services.all()).count()

    def __str__(self):
        return f'{self.project} - {self.title}'

class HTTPCodeService(models.Model):
    url = models.URLField(max_length=512, blank=False)
    tls_skip_verify = models.BooleanField("Ignore unsecure SSL", default=False, help_text="Might be needed for monitoring some CDN or object storage directly.")
    service = models.OneToOneField(
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
    service = models.OneToOneField(
        Service,
        on_delete = models.CASCADE,
        related_name = "httpmockedcode",
    )

    def url(self):
        """
            Return the url to use within prometheus to get the HTTP code value
        """
        result = ''

        # Select protocol between http and https
        if settings.FORCE_HTTPS:
            result += 'https://'
        else:
            result += 'http://'

        # Handle localhost as host.docker.internal for docker
        if settings.DOMAIN != 'localhost' and not is_private_ipv4(settings.DOMAIN):
            result += f'{settings.DOMAIN}'
        else:
            result += 'host.docker.internal'

        # If port if custom, we add it in the url
        if settings.PORT and settings.PORT != '80' and settings.PORT != '443':
            result += f':{settings.PORT}'

        # url defined by django app
        result += f'/healthy/{self.id}/'

        return result
