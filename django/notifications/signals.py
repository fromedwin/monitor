from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from incidents.models import Incident
from .utils import send_emails

@receiver(pre_save, sender=Incident)
def send_notifications(sender, instance=None, created=False, **kwargs):

    is_created = not bool(instance.pk)
    is_modified = False

    if not is_created:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            is_modified = True
        if old_instance.severity != instance.severity:
            is_modified = True

    if is_created or is_modified:
        # Test if instance has related model service
        if 'service_incidents' in instance.__dict__ and instance.service_incidents:
            emails = instance.service_incidents.service.project.emails.all()
            if len(emails) and emails[0]:
                send_emails(instance, emails[0].email)
