from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def getStatus(alert):
    if alert["status"] == "resolved":
        return INCIDENT_STATUS['RESOLVED']
    if alert["status"] == "firing":
        return INCIDENT_STATUS['FIRING']
    return INCIDENT_STATUS['UNKNOWN']

def getSeverity(alert):
    if alert["labels"]["severity"] == "warning":
        return INCIDENT_SEVERITY['WARNING'] 
    if alert["labels"]["severity"] == "critical":
        return INCIDENT_SEVERITY['CRITICAL']
    return INCIDENT_SEVERITY['UNKNOWN'] 

def getStartsAt(alert, settings):
    starts_at = timezone.make_aware(timezone.datetime.strptime(alert["startsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))
    # Based on the severity, we update starting time to include the time before the alert
    severity = getSeverity(alert)
    if severity == INCIDENT_SEVERITY['CRITICAL']:
        starts_at = starts_at - timedelta(minutes=settings.IS_SERVICE_DOWN_TRIGGER_OUTRAGE_MINUTES)
    elif severity == INCIDENT_SEVERITY['WARNING']:
        starts_at = starts_at - timedelta(minutes=settings.IS_SERVICE_DOWN_TRIGGER_WARNING_MINUTES)
    return starts_at

def getEndsAt(alert):
    ends_at = None
    if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
        ends_at = timezone.make_aware(timezone.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))
    return ends_at
