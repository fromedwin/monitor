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

from alerts.models import Alerts
from availability.models import Service
from projects.models import Project

from .models import Incident, UnknownIncident, ServiceIncident
from .handlers.handleUnkownIncident import handleUnkownIncident
from .handlers.handleServiceIncident import handleServiceIncident
from .utils import getStatus, getSeverity, getStartsAtWithDelay, getEndsAt


from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleAlert(request, alert):

    incident = Incident(
        starts_at = getStartsAtWithDelay(alert),
        ends_at = getEndsAt(alert),
        status = getStatus(alert),
        severity = getSeverity(alert),
        json = json.dumps(alert, indent=2, sort_keys=True),
    )

    # We get db alert model for foreign key based on alert name
    alert_object = Alerts.objets.get(name=alert["labels"]["alertname"])

    if not alert_object:
        unknown_incident = UnknownIncident(
            incident = incident,
            alert_name = alert["labels"]["alertname"],
            summary = alert["annotations"]["summary"],
            description = alert["annotations"]["description"],
        )
        handleUnkownIncident(unknown_incident)
        
    elif alert["labels"]["service"]:
        try:
            service = Service.objects.get(pk=alert["labels"]["service"])
            service_incident = ServiceIncident(
                incident = incident,
                alert = alert_object,
                service = service,
            )
            handleServiceIncident(service_incident)
        except Service.DoesNotExist:
            # If user delete a service with an open alert then prometeheus close the alert,
            # alert manager report the alert as close for deleted service and was returning 500.
            # Now return 200.
            pass
