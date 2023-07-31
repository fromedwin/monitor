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
from alerts.models import ProjectIncident
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleProjectAlert(alert, status, severity, json_formated, startsAt, endsAt):
    project = None

    if alert["labels"]["project"]:
        # If user delete a project while an alert is open, alertmanager still send a resolve
        # This will ignore the resolve or new update
        try:
            project = Project.objects.get(pk=alert["labels"]["project"])
        except:
            pass

    # If we receive resolved, we delete firing with same startAt and fingerprint
    try:
        if status == INCIDENT_STATUS['RESOLVED'] or status == INCIDENT_STATUS['FIRING']:
            items = ProjectIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=INCIDENT_STATUS['FIRING'])
            for item in items:
                item.delete()
    except:
        pass

    if project:
        ProjectIncident.objects.create(
            project=project,
            startsAt=startsAt,
            endsAt=endsAt,
            fingerprint=alert["fingerprint"],
            instance=alert["labels"]["instance"],
            summary=alert["annotations"]["summary"],
            description=alert["annotations"]["description"],
            severity=severity,
            status=status,
            json=json_formated)
