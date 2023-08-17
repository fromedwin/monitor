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

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleUnkownIncident(unknownIncident):
    # If we receive resolved, we delete firing with same start_at and fingerprint
    try:
        if unknownIncident.incident.status == INCIDENT_STATUS['RESOLVED'] or unknownIncident.incident.status == INCIDENT_STATUS['FIRING']:
            items = UnknownIncident.objects.filter(
                incident__starts_at=unknownIncident.incident.startsAt,
                incident__ends_at__isnull=True,
                summary=unknownIncident.summary, 
                description=unknownIncident.description)
        else:
            unknownIncident.incident.save()
            unknownIncident.save()
    except:
        pass

