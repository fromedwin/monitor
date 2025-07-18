from django.db import models
from projects.models import Pages
from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

MAX_REPORTS_TO_KEEP = 4

def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.page.directory_path(), filename)

def delete_old_reports(report):
    # Select all reports order from recent to old and if more than 4 delete all older than the 4 more recent
    reports = LighthouseReport.objects.filter(page=report.page).order_by('-creation_date')
    if reports.count() > MAX_REPORTS_TO_KEEP:
        for r in reports[MAX_REPORTS_TO_KEEP:]:
            r.delete()

# Create your models here.
class LighthouseReport(models.Model):
    """
    A django model for a lighthouse report
    """
    page = models.ForeignKey(
        Pages,
        on_delete = models.CASCADE,
        related_name = "lighthouse_report",
    )
    screenshot = models.ImageField(upload_to=user_directory_path, blank=True, null=True, help_text="Lighthouse screenshot")
    form_factor = models.IntegerField(choices=LIGHTHOUSE_FORMFACTOR_CHOICES, default=LIGHTHOUSE_FORMFACTOR_CHOICES[0][0], help_text="Lighthouse form factor, mobile or desktop")
    score_performance = models.FloatField(blank=True, null=True, help_text="Lighthouse performance score")
    score_accessibility = models.FloatField(blank=True, null=True, help_text="Lighthouse accessibility score")
    score_best_practices = models.FloatField(blank=True, null=True, help_text="Lighthouse best practices score")
    score_seo = models.FloatField(blank=True, null=True, help_text="Lighthouse seo score")
    score_pwa = models.FloatField(blank=True, null=True, help_text="Lighthouse pwa score")
    report_json_file = models.FileField(upload_to=user_directory_path, blank=True, null=True, help_text="Lighthouse report")
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    celery_task_log = models.ForeignKey(
        'logs.CeleryTaskLog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lighthouse',
        help_text="Celery task log associated with this lighthouse report"
    )

    def save(self, *args, **kwargs):
        super(LighthouseReport, self).save(*args, **kwargs)
        delete_old_reports(self)

    def __str__(self):
        return f'Performance {self.page.id} - {self.creation_date}'
