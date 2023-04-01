from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from constants import STATUS, INCIDENT_SEVERITY

def send_emails(incident, email):

    status = 'Unkonwn'

    if incident.severity == INCIDENT_SEVERITY['WARNING']:
        status = 'warning'
    elif incident.severity == INCIDENT_SEVERITY['CRITICAL']:
        status = 'critical'

    subject = f'[{status}] {incident.summary}'
    html_message = render_to_string('notifications/emails/instance_down_email.html', {'incident': incident})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    send_mail(
        subject,
        plain_message,
        from_email,
        to,
        html_message=html_message,
        fail_silently=False,
    )
