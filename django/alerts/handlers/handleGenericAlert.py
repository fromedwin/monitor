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
from alerts.models import GenericIncident
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleGenericAlert(alert, status, severity, json_formated, startsAt, endsAt):
    # If we receive resolved, we delete firing with same startAt and fingerprint
    try:
        if status == INCIDENT_STATUS['RESOLVED'] or status == INCIDENT_STATUS['FIRING']:
            items = GenericIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=INCIDENT_STATUS['FIRING'])
            for item in items:
                startsAt = item.startsAt
                item.delete()
    except:
        pass

    GenericIncident.objects.create(
        startsAt=startsAt,
        endsAt=endsAt,
        fingerprint=alert["fingerprint"],
        instance=alert["labels"]["instance"] if 'instance' in alert["labels"] else None,
        summary=alert["annotations"]["summary"],
        description=alert["annotations"]["description"],
        severity=severity,
        status=status,
        json=json_formated)

