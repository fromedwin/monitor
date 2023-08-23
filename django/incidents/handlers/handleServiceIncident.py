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
from incidents.models import ServiceIncident
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleServiceIncident(serviceIncident):
    try:
        items = ServiceIncident.objects.filter(
            incident__ends_at__isnull=True,
            service=serviceIncident.service, 
            alert=serviceIncident.alert)
        if len(items) >= 1:
            for item in items:

                if item.incident.severity == INCIDENT_SEVERITY['WARNING'] and \
                    serviceIncident.incident.severity == INCIDENT_SEVERITY['CRITICAL']:
                    item.incident.severity = INCIDENT_SEVERITY['CRITICAL']
                item.incident.status = serviceIncident.incident.status

                if serviceIncident.incident.starts_at < item.incident.starts_at:
                    item.incident.starts_at = serviceIncident.incident.starts_at

                item.incident.ends_at = serviceIncident.incident.ends_at
                item.incident.json = serviceIncident.incident.json
                item.incident.save()
        else:
            if serviceIncident.incident.status != INCIDENT_STATUS['RESOLVED']:
                serviceIncident.incident.save()
                serviceIncident.save()
    except Exception as err:
        if settings.DEBUG is True:
            print(err)
        raise err
