from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from core.utils import is_private_ipv4

class Project(models.Model):
    """
    A user own a project he want to monitor and work on.
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "projects",
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

        value = round(100 - total_unavailability * 100 / total_second, 3)

        if value < 0:
            return 0
        return value

    def incidents_count(self):
        from incidents.models import InstanceDownIncident, ProjectIncident
        return InstanceDownIncident.objects.filter(service__in=self.services.all()).count() + ProjectIncident.objects.filter(project=self).count()

    def url(self):
        return f"/project/{self.id}/"

    def performance_score(self):
        result = {
            'score_performance': None,
            'score_accessibility': None,
            'score_best_practices': None,
            'score_seo': None,
            'score_pwa': None,
        }
        last_run = None
        performances = self.performances.all()

        # If performances are available, we add all p=score for all page then divide by page number
        if len(performances) > 0:
            for key in result.keys():
                if result[key] is None:
                    result[key] = 0

            try:
                for performance in performances:
                    score = performance.last_score()
                    if performance.reports.last().creation_date:
                        for key in score.keys():
                            if score[key]:
                                result[key] = result[key] + score[key]
                        if last_run is None or last_run < performance.reports.last().creation_date:
                            last_run = performance.reports.last().creation_date
            except:
                pass
            for key in score.keys():
                result[key] = result[key] / len(performances)

        # If no report, we change None to '--' so eschart can display empty diagram
        for key in result.keys():
            if result[key] is None:
                result[key] = '--'

        result['last_run'] = last_run
        return result

    def __str__(self):
        return self.title
