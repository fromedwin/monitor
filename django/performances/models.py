import os
from django.db import models
from projects.models import Project
from django.conf import settings
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify

from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

class Performance(models.Model):
    """
    A performance is a url to run google lighthouse on at regular intervals
    """
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "performances",
    )
    url = models.URLField(max_length=512, blank=False, help_text="Should start with http:// or https://")
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    request_run = models.BooleanField(default=False, help_text="Request a run")
    last_request_date = models.DateTimeField(blank=True, null=True, help_text="Last request date")

    @property
    def status(self):
        return 'Waiting for a worker'

    def last_score(self):
        performance = self.reports.last()
        if performance:
            return {
                'score_performance': performance.score_performance,
                'score_accessibility': performance.score_accessibility,
                'score_best_practices': performance.score_best_practices,
                'score_seo': performance.score_seo,
                'score_pwa': performance.score_pwa,
            }
        else:
            return {
                'score_performance': None,
                'score_accessibility': None,
                'score_best_practices': None,
                'score_seo': None,
                'score_pwa': None,
            }

    def __str__(self):
        return f'{self.url}'

    def directory_path(self):
        user_pk = self.project.user.pk
        project_pk = self.project.pk
        return f'/{user_pk}/{project_pk}/performances/{self.pk}'

    def delete(self):
        super().delete()
        if default_storage.exists(self.directory_path()):
            try:
                # Deletes the performance folder.
                # Content has already been deleted by cascading.
                default_storage.delete(self.directory_path())
            except Exception as e:
                print(f"Error deleting folder: {e}")

"""
    REPORT MODEL
"""
def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.performance.directory_path(), filename)

def delete_old_reports(report):
    # Select all reports order from recent to old and if more than 4 delete all older than the 4 more recent
    reports = Report.objects.filter(performance=report.performance).order_by('-creation_date')
    if reports.count() > 4:
        for r in reports[4:]:
            r.delete()

class Report(models.Model):
    """
    A django model for a lighthouse report
    """
    performance = models.ForeignKey(
        Performance,
        on_delete = models.CASCADE,
        related_name = "reports",
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

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        delete_old_reports(self)

    def __str__(self):
        return f'Performance {self.performance.id} - {self.creation_date}'

class ReportScreenshots(models.Model):
    """
    A django model for a lighthouse report screenshot
    """
    report = models.ForeignKey(
        Report,
        on_delete = models.CASCADE,
        related_name = "screenshots",
    )
    screenshot = models.ImageField(upload_to='lighthouse_screenshots', blank=True, null=True, help_text="Lighthouse screenshot")
    timestamp = models.DateTimeField(blank=True, null=True, help_text="Screenshot")
    timing = models.IntegerField(blank=True, null=True, help_text="Lighthouse timing")
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")

    def __str__(self):
        return f'Report {self.report.id} - {self.creation_date}'
