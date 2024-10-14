from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from incidents.models import Incident
from .models import Notification
from .utils import send_emails
from constants import INCIDENT_SEVERITY, INCIDENT_STATUS, NOTIFICATION_SEVERITY

@receiver(pre_save, sender=Incident)
def create_notifications(sender, instance=None, **kwargs):
    is_created = not bool(instance.pk)
    is_modified = False

    if not is_created:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            is_modified = True
        if old_instance.severity != instance.severity:
            is_modified = True

    if is_created or is_modified:
        if instance.status == INCIDENT_STATUS['RESOLVED']:
            message = instance.html_resolved
            severity = NOTIFICATION_SEVERITY['RESOLVED']
        elif instance.severity == INCIDENT_SEVERITY['WARNING']:
            message = instance.html_warning
            severity = NOTIFICATION_SEVERITY['WARNING']
        elif instance.severity == INCIDENT_SEVERITY['CRITICAL']:
            message = instance.html_critical
            severity = NOTIFICATION_SEVERITY['CRITICAL']
        else:
            message = None

        if message:
            Notification(
                message = message,
                project = instance.service.project if instance.service else None,
                service = instance.service if instance.service else None,
                severity = severity,
            ).save()


@receiver(pre_save, sender=Notification)
def send_notifications(sender, instance=None, **kwargs):

    is_created = not bool(instance.pk)
    
    if is_created:
        # Test if instance has related model service
        try:
            if instance.service:
                emails = instance.service.project.emails.all()
                if len(emails) and emails[0]:
                    send_emails(instance, emails[0].email)
        except Exception as e:
            print(e)
            pass
