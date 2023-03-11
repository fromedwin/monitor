from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from fromedwin.utils import is_private_ipv4

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
    is_favorite = models.BooleanField('Is favorite', default=False, help_text="Favorite project are highlighted and first shown when possible.")
    enable_public_page = models.BooleanField('Enable public page', default=False, help_text="Will enable the public page to share current project status")

    def is_offline(self):
        return self.services.filter(instancedownincidents__status=2, is_critical=True, is_enabled=True, instancedownincidents__severity=2)

    def is_degraded(self):
        return self.services.filter(instancedownincidents__status=2, is_critical=False, is_enabled=True, instancedownincidents__severity=2)

    def is_warning(self):
        return self.services.filter(instancedownincidents__status=2, is_critical=True, is_enabled=True, instancedownincidents__severity=1)

    def availability(self, days=30):

        from alerts.models import InstanceDownIncident

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

    def incidents_count(self):
        from alerts.models import InstanceDownIncident, ProjectIncident
        return InstanceDownIncident.objects.filter(service__in=self.services.all()).count() + ProjectIncident.objects.filter(project=self).count()

    def url(self):
        return f"/project/{self.id}"

    def __str__(self):
        return self.title
