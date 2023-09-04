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

from incidents.utils import getStatus, getSeverity
from incidents.models import UnknownIncident
from projects.models import Project
from availability.models import Service

from django.conf import settings

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleUnkownIncident(unknownIncident):
    # If we receive resolved, we delete firing with same start_at and fingerprint
    try:
        if  unknownIncident.incident.status == INCIDENT_STATUS['RESOLVED'] or \
            unknownIncident.incident.status == INCIDENT_STATUS['FIRING']:
            items = UnknownIncident.objects.filter(
                starts_at=unknownIncident.incident.starts_at,
                ends_at__isnull=True,
                alert_name=unknownIncident.alert_name, 
                summary=unknownIncident.summary, 
                description=unknownIncident.description)

            if len(items) >= 1:
                for item in items:
                    if item.incident.severity == INCIDENT_SEVERITY['WARNING'] and \
                        unknownIncident.incident.severity == INCIDENT_SEVERITY['CRITICAL']:
                        item.incident.severity = INCIDENT_SEVERITY['CRITICAL']

                    item.incident.status = unknownIncident.incident.status
                    item.incident.starts_at = unknownIncident.incident.starts_at
                    item.incident.ends_at = unknownIncident.incident.ends_at
                    item.incident.save()
            else:
                unknownIncident.incident.save()
                unknownIncident.save()
        else:
            unknownIncident.incident.save()
            unknownIncident.save()
    except Exception as err:
        if settings.DEBUG:
            print(err)
        raise err
