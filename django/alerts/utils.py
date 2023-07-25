import datetime
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

def getStartsAtWithDelay(alert):
    startsAt = timezone.make_aware(datetime.datetime.strptime(alert["startsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

    if alert["labels"]["alertname"] == "InstanceDown":

        severity = getSeverity(alert)
        if severity == INCIDENT_SEVERITY['CRITICAL']:
            startsAt = startsAt - timedelta(minutes=settings.IS_SERVICE_DOWN_TRIGGER_OUTRAGE_MINUTES)
        elif severity == INCIDENT_SEVERITY['WARNING']:
            startsAt = startsAt - timedelta(minutes=2)

    return startsAt
