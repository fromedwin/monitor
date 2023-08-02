from django.db import models

from projects.models import Project

class Emails(models.Model):
    """
    Assign an email to which notifications will be sent
    """
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "emails",
        blank=False
    )
    email = models.EmailField(max_length=254, blank=False)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
