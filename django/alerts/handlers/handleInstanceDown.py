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

    try:
        service = Service.objects.get(pk=alert["labels"]["service"])
        # Try to get object with fingerprint
        incident = InstanceDownIncident.objects.filter(service=service, startsAt=startsAt).first()

        if incident:

            # we decect if this is a repeat or a change of state.
            if  incident.severity == INCIDENT_SEVERITY['WARNING'] and severity == INCIDENT_SEVERITY['CRITICAL'] or \
                incident.status == INCIDENT_STATUS['FIRING'] and status == INCIDENT_STATUS['RESOLVED']:

                incident.startsAt = startsAt
                incident.endsAt = endsAt
                incident.status = status
                incident.severity = severity
                incident.json_formated = json_formated
                incident.save()

        else:

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
    except Service.DoesNotExist:
        # If user delete a service with an open alert then prometeheus close the alert,
        # alert manager report the alert as close for deleted service and was returning 500.
        # Now return 200.
        pass

