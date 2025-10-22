from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import ProjectReport
from constants import NOTIFICATION_SEVERITY

@receiver(post_save, sender=ProjectReport)
def send_report_notification_email(sender, instance, created, **kwargs):
    """
    Send email notification when a new report is created
    """
    if created:
        try:
            # Get the project and user
            project = instance.project
            user = project.user
            
            # Check if user has email
            if not user.email:
                return
            
            # Prepare email content
            subject = f"📊 New Report Available - {project.title}"
            
            # Create the report URL
            report_url = f"{settings.BACKEND_URL}/project/{project.id}/reports/"
            
            # Render email template
            html_message = render_to_string('reports/emails/report_available.html', {
                'project': project,
                'report': instance,
                'report_url': report_url,
                'user': user,
            }).strip()
            
            plain_message = strip_tags(html_message).strip()
            
            # Send email
            from_email = f"{getattr(settings, 'CONTACT_NAME', 'Monitor')} <{getattr(settings, 'CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)}>"
            to = [user.email]
            
            send_mail(
                subject,
                plain_message,
                from_email,
                to,
                html_message=html_message,
                fail_silently=True,  # Don't fail if email sending fails
            )
            
        except Exception as e:
            # Log the error but don't fail the report creation
            print(f"Failed to send report notification email: {e}")
            pass
