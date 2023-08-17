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

from .handler import handleAlert
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

@api_view(["POST"])
def webhook(request):
    if request.data["alerts"]:
        # We receive batched alerts from alertmanager and handle them one by
        for alert in request.data["alerts"]:
            handleAlert(request, alert)

    return Response()
