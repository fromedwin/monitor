import os
from django.db import models
from projects.models import Project
from django.conf import settings

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
    last_request_date = models.DateTimeField(blank=True, null=True, help_text="Last request date")

    @property
    def status(self):
        return 'Waiting for a worker'

    def __str__(self):
        return f'{self.url}'

def user_directory_path(instance, filename):
    return 'performance/reports/{0}/{1}'.format(instance.performance.pk, filename)

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
    form_factor = models.IntegerField(choices=LIGHTHOUSE_FORMFACTOR_CHOICES, default=LIGHTHOUSE_FORMFACTOR_CHOICES[0][0], help_text="Lighthouse form factor")
    score_performance = models.FloatField(blank=True, null=True, help_text="Lighthouse performance score")
    score_accessibility = models.FloatField(blank=True, null=True, help_text="Lighthouse accessibility score")
    score_best_practices = models.FloatField(blank=True, null=True, help_text="Lighthouse best practices score")
    score_seo = models.FloatField(blank=True, null=True, help_text="Lighthouse seo score")
    score_pwa = models.FloatField(blank=True, null=True, help_text="Lighthouse pwa score")
    report_json_file = models.FileField(upload_to='lighthouse_reports', blank=True, null=True, help_text="Lighthouse report")
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")

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
