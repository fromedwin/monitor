from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def project_favicon_path(self, filename):
    return f'{self.directory_path()}/favicons/{filename}'

# List of status for favicon task
FAVICON_TASK_STATUS = (
    ('PENDING', 'Pending'),
    ('SUCCESS', 'Success'),
    ('FAILURE', 'Failure'),
    ('UNKNOWN', 'Unknown'),
)

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
    url = models.URLField(max_length=512, blank=True, null=True, help_text="Application's URL")
    is_favorite = models.BooleanField('Is favorite', default=False, help_text="Favorite project are highlighted and first shown when possible.")
    enable_public_page = models.BooleanField('Enable public page', default=False, help_text="Will enable the public page to share current project status")
    # Handle favicon
    favicon = models.ImageField(upload_to=project_favicon_path, blank=True, null=True, help_text="Application's favicon")
    favicon_task_status = models.CharField(max_length=16, choices=FAVICON_TASK_STATUS, default='UNKNOWN', help_text="Favicon task status")
    favicon_last_edited = models.DateTimeField(editable=False, help_text="Last time favicon was edited", default=timezone.now)

    def is_offline(self):
        return self.services.filter(
            incidents__status = 2, 
            is_critical = True, 
            is_enabled = True, 
            incidents__severity = 2
        )

    def is_degraded(self):
        return self.services.filter(
            incidents__status = 2, 
            is_critical = False, 
            is_enabled = True, 
            incidents__severity = 2
        )

    def is_warning(self):
        return self.services.filter(
            incidents__status = 2, 
            is_critical = True, 
            is_enabled = True, 
            incidents__severity = 1
        )

    def availability(self, days=30):

        from incidents.models import Incident

        total_second = days * 24 * 60 * 60
        start_date = timezone.now() - timezone.timedelta(days=days)

        alerts = Incident.objects.filter(
            service__in=self.services.filter(is_critical=True), 
            severity=2, 
            ends_at__gte=start_date) | \
            Incident.objects.filter(
                service__in=self.services.filter(is_critical=True), 
                severity=2, 
                ends_at__isnull=True)

        total_unavailability = 0
        for alert in alerts:
            if not alert.ends_at:
                total_unavailability += (timezone.now() - alert.starts_at).seconds
            elif alert.starts_at < start_date:
                total_unavailability += (alert.ends_at - start_date).seconds
            else:
                total_unavailability += alert.duration.seconds

        value = round(100 - total_unavailability * 100 / total_second, 3)

        if value < 0:
            return 0
        return value
    
    def pathname(self):
        return f"/project/{self.id}/"

    def incidents_count(self):
        from incidents.models import Incident
        return Incident.objects.filter(service__in=self.services.all()).count()

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

    def directory_path(self):
        return f'user_{self.user.pk}/prjct_{self.pk}'

    def __str__(self):
        return self.title

