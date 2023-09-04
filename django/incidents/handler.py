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

from availability.models import Service
from projects.models import Project

from .models import Incident
from .utils import getStatus, getSeverity, getStartsAt, getEndsAt

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleAlert(request, alert):

    incident = Incident(
        alert_name = alert["labels"]["alertname"],
        starts_at = getStartsAt(alert),
        ends_at = getEndsAt(alert),
        status = getStatus(alert),
        severity = getSeverity(alert),
        summary = alert["annotations"]["summary"],
        description = alert["annotations"]["description"],
        json = json.dumps(alert, indent=2, sort_keys=True),
        service = Service.objects.get(pk=alert["labels"]["service"]) if alert["labels"]["service"] else None,
    )

    try:
        if  incident.status == INCIDENT_STATUS['RESOLVED'] or \
            incident.status == INCIDENT_STATUS['FIRING']:
            items = Incident.objects.filter(
                starts_at=incident.starts_at,
                ends_at__isnull=True,
                alert_name=incident.alert_name, 
                summary=incident.summary, 
                description=incident.description)

            if len(items) >= 1:
                for item in items:
                    if item.severity == INCIDENT_SEVERITY['WARNING'] and \
                        incident.severity == INCIDENT_SEVERITY['CRITICAL']:
                        item.severity = INCIDENT_SEVERITY['CRITICAL']

                    item.status = incident.status
                    item.starts_at = incident.starts_at
                    item.ends_at = incident.ends_at
                    item.json = incident.json
                    item.save()
            else:
                incident.save()
        else:
            incident.save()
    except Exception as err:
        if settings.DEBUG:
            print(err)
        raise err
