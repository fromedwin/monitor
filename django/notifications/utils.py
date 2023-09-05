from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from constants import NOTIFICATION_SEVERITY

def send_emails(notification, email):

    subject = ''

    if notification.severity == NOTIFICATION_SEVERITY['WARNING']:
        subject = "⚠️ " + notification.service.project.title+ " - " + notification.service.title

    if notification.severity == NOTIFICATION_SEVERITY['CRITICAL']:
        subject = "❌ " + notification.service.project.title+ " - " + notification.service.title

    if notification.severity == NOTIFICATION_SEVERITY['RESOLVED']:
        subject = "✅ " + notification.service.project.title+ " - " + notification.service.title

    if notification.severity == NOTIFICATION_SEVERITY['UNKNOWN']:
        subject = "🤖 - " + notification.service.project.title+ " - " + notification.service.title

    html_message = render_to_string('notifications/emails/notification_email.html', {
        'notification': notification, 
    }).strip()
    plain_message = strip_tags(html_message).strip()
    from_email = f"{settings.CONTACT_NAME} <{settings.CONTACT_EMAIL}>"
    to = [email]

    send_mail(
        subject,
        plain_message,
        from_email,
        to,
        html_message=html_message,
        fail_silently=False,
    )
