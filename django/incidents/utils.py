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
    starts_at = timezone.make_aware(datetime.datetime.strptime(alert["startsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))
    return starts_at

def getEndsAt(alert):
    ends_at = None
    if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
        ends_at = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))
    return ends_at
