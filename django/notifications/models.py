from django.db import models

from projects.models import Project
from availability.models import Service
from constants import NOTIFICATION_SEVERITY_CHOICES, NOTIFICATION_SEVERITY

class Notification(models.Model):
    """
    This is a message bubble as notification from Edwin to display in chat
    """
    date = models.DateTimeField(auto_now_add = True)
    message = models.TextField(blank = False)
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "notifications",
        blank = True
    )
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE,
        related_name = "notifications",
        blank = True
    )
    severity = models.IntegerField(
        choices = NOTIFICATION_SEVERITY_CHOICES, 
        default = NOTIFICATION_SEVERITY['UNKNOWN'], 
        blank = False
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

class Emails(models.Model):
    """
    Assign an email to which notifications will be sent
    """
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "emails",
        blank = False
    )
    email = models.EmailField(max_length=254, blank=False)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
