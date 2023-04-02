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

from .models import GenericIncident, InstanceDownIncident, ProjectIncident
from .utils import getStatus, getSeverity, getStartsAtWithDelay
from .handlers.handleInstanceDown import handleInstanceDown
from .handlers.handleProjectAlert import handleProjectAlert
from .handlers.handleGenericAlert import handleGenericAlert
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

def handleAlert(request, alert):

    # Prepare data to handle
    status = getStatus(alert)
    severity = getSeverity(alert)
    json_formated = json.dumps(alert, indent=2, sort_keys=True)

    # Handle date range
    startsAt = getStartsAtWithDelay(alert)
    endsAt = None
    if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
        endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

    handler = handleGenericAlert

    # WE RECEIVE AN UPDATE ABOUT AN INSTANCE DOWN EVENT
    if alert["labels"]["alertname"] == "InstanceDown":
        handler = handleInstanceDown

    elif "project" in alert["labels"]:
        handler = handleProjectAlert
        
    handler(alert, status, severity, json_formated, startsAt, endsAt)
