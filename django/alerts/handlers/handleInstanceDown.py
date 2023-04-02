import json
import datetime
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from alerts.utils import getStatus, getSeverity
from alerts.models import InstanceDownIncident
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleInstanceDown(alert, status, severity, json_formated, startsAt, endsAt):
    service = None
    if alert["labels"]["service"]:
        # If user delete a service while an alert is open, alertmanager still send a resolve
        # This will ignore the resolve or new update
        try:
            service = Service.objects.get(pk=alert["labels"]["service"])
        except:
            pass

    ignore_warning_resolved = False

    # If we receive a warning resolve
    if status == INCIDENT_STATUS['RESOLVED'] and severity == INCIDENT_SEVERITY['WARNING'] :
        # If there is a critical at the same time, we ignore warning resolve
        if InstanceDownIncident.objects.filter(startsAt=startsAt, severity=INCIDENT_SEVERITY['CRITICAL'], service=service):
            ignore_warning_resolved = True

    # If we receive resolved, we delete firing with same startAt and fingerprint
    try:
        # We might receive multiple critical event as every 12h alertmanager repeat the critical event. 
        # This is about deleting all copy.
        if status == INCIDENT_STATUS['RESOLVED'] or status == INCIDENT_STATUS['FIRING']:
            items = InstanceDownIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=INCIDENT_STATUS['FIRING'])
            for item in items:
                item.delete()
    except:
        pass

    # ignore_warning_resolved is True if a critical_resolved also exist
    if not ignore_warning_resolved and service:
        InstanceDownIncident.objects.create(
            service=service,
            startsAt=startsAt,
            endsAt=endsAt,
            fingerprint=alert["fingerprint"],
            instance=alert["labels"]["instance"],
            summary=alert["annotations"]["summary"],
            description=alert["annotations"]["description"],
            severity=severity,
            status=status,
            json=json_formated)
