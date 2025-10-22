from django.db import models

# Create your models here.
from projects.models import Project

class ProjectReport(models.Model):
    """
    Very basic model for a report, storing JSON data.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_report")
    data = models.JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)
    celery_task_log = models.ForeignKey(
        'logs.CeleryTaskLog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports',
        help_text="Celery task log associated with this project report"
    )

    def save(self, *args, **kwargs):
        super(ProjectReport, self).save(*args, **kwargs)

    def __str__(self):
        return f'Report {self.project.title} - {self.creation_date:%Y-%m-%d}'

    class Meta:
        ordering = ['-creation_date']


