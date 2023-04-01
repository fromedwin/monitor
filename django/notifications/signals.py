from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from alerts.models import InstanceDownIncident
from .utils import send_emails

@receiver(post_save, sender=InstanceDownIncident)
def send_notifications(sender, instance=None, created=False, **kwargs):
    if created:
        emails = instance.service.project.emails.all()
        if len(emails) and emails[0]:
            send_emails(instance, emails[0].email)
