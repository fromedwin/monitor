from django.db import models
from projects.models import Project

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

class Report(models.Model):
    """
    A django model for a lighthouse report
    """
    performance = models.ForeignKey(
        Performance,
        on_delete = models.CASCADE,
        related_name = "reports",
    )
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")
    lighthouse_formFactor = models.IntegerField(choices=LIGHTHOUSE_FORMFACTOR_CHOICES, default=LIGHTHOUSE_FORMFACTOR_CHOICES[0][0], help_text="Lighthouse form factor")
    lighthouse_score_performance = models.IntegerField(blank=True, null=True, help_text="Lighthouse performance score")
    lighthouse_score_accessibility = models.IntegerField(blank=True, null=True, help_text="Lighthouse accessibility score")
    lighthouse_score_bestPractices = models.IntegerField(blank=True, null=True, help_text="Lighthouse best practices score")
    lighthouse_score_seo = models.IntegerField(blank=True, null=True, help_text="Lighthouse seo score")
    lighthouse_score_pwa = models.IntegerField(blank=True, null=True, help_text="Lighthouse pwa score")
    # Lighthouse report
    lighthouse_report = models.JSONField(blank=False, null=False, editable=False)

    def __str__(self):
        return f'Performance {self.performance.id} - {self.creation_date}'
