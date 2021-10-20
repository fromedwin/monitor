from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Application(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "applications",
    )
    title = models.CharField(max_length=128, blank=False)
    enable_public_status = models.BooleanField(default=False)

    def is_healthy(self):
        return not self.services.filter(instancedownalerts__status=2)

    def is_critical(self):
        return self.services.filter(instancedownalerts__status=2, is_critical=True)

    def is_warning(self):
        return self.services.filter(instancedownalerts__status=2, is_critical=False)

    def __str__(self):
        return self.title

class Service(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete = models.CASCADE,
        related_name = "services",
    )
    title = models.CharField(max_length=128, blank=False)
    url = models.URLField(max_length=512, blank=False)
    is_public = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)
    is_critical = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Creation date")

    def __str__(self):
        return f'{self.application} - {self.title}'

class Metrics(models.Model):
    """
    Fetch {{url}}/metrics within prometheus
    Can be used for node_explorer or custom metrics
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "metrics",
    )
    url = models.URLField(max_length=512, blank=False)
    is_enabled = models.BooleanField(default=True)
