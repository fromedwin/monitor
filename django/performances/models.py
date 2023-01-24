from django.db import models
from projects.models import Project

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

    @property
    def status(self):
        return 'Waiting for a worker '

    def __str__(self):
        return f'{self.url}'
