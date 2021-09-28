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
