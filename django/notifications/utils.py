from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def send_emails(incident, email):

    status = 'Unknown'

    if incident.severity == INCIDENT_SEVERITY['WARNING']:
        status = 'Warning'
    elif incident.severity == INCIDENT_SEVERITY['CRITICAL']:
        status = 'Critical'

    if incident.status == INCIDENT_STATUS['RESOLVED']:
        status = 'Resolved'

    summary = ''
    if 'unknown_incidents' in incident:
        summary = incident.unknown_incidents.summary
    if 'service_incidents' in incident:
        summary = incident.service_incidents.alert.summary

    subject = f'[{status}] {summary}'
    html_message = render_to_string('notifications/emails/instance_down_email.html', {'incident': incident})
    plain_message = strip_tags(html_message)
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
