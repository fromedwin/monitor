from django.db import models

# Create your models here.

class CeleryTaskLog(models.Model):
    """
    Simple model to log Celery task execution
    """
    from projects.models import Project

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='celery_task_logs',
        help_text="Project associated with this Celery task log"
    )
    task_name = models.CharField(max_length=255)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'celery_task_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task_name} - {self.created_at}"
