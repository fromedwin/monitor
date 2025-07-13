from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# List of status for tasks
TASK_STATUS = (
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
    # Handle sitemaps
    sitemap_task_status = models.CharField(max_length=16, choices=TASK_STATUS, default='UNKNOWN', help_text="Sitemap task status")
    sitemap_last_edited = models.DateTimeField(help_text="Last time sitemap was edited", default=timezone.now)

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
        from lighthouse.models import LighthouseReport
        from django.db.models import Avg
        
        reports = LighthouseReport.objects.filter(page__project=self)
        if reports.exists():
            averages = reports.aggregate(
                avg_performance=Avg('score_performance'),
                avg_accessibility=Avg('score_accessibility'),
                avg_best_practices=Avg('score_best_practices'),
                avg_seo=Avg('score_seo'),
                avg_pwa=Avg('score_pwa'),
            )
            return {
                'score_performance': averages['avg_performance'],
                'score_accessibility': averages['avg_accessibility'],
                'score_best_practices': averages['avg_best_practices'],
                'score_seo': averages['avg_seo'],
                'score_pwa': averages['avg_pwa'],
            }
        return None


    def directory_path(self):
        return f'user_{self.user.pk}/prjct_{self.pk}'

    def __str__(self):
        return self.title


class Pages(models.Model):
    """
    List of all urls identified for a project based on url value
    """
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "pages",
    )
    url = models.URLField(max_length=512, blank=False, help_text="URL to monitor")
    title = models.CharField(max_length=128, blank=True, help_text="Page title")
    description = models.TextField(blank=True, help_text="Page description")
    created_at = models.DateTimeField(auto_now_add=True)
    sitemap_last_seen = models.DateTimeField(help_text="Last time sitemap was reported", null=True, blank=True)
    scraping_last_seen = models.DateTimeField(help_text="Last time scraping was run", null=True, blank=True)
    lighthouse_last_request = models.DateTimeField(help_text="Last time lighthouse was requested", null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'url'], name='unique_page_project_url')
        ]