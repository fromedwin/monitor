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
from projects.models import Project, Service

from constants import INCIDENT_STATUS, INCIDENT_SEVERITY

@api_view(["POST"])
def webhook(request):
    if request.data["alerts"]:
        # We receive batched alerts from alertmanager and handle them one by
        for alert in request.data["alerts"]:
            json_formated = json.dumps(alert, indent=2, sort_keys=True)

            # Status is 0 if resolved and 1 if firing
            status = INCIDENT_STATUS['UNKNOWN']
            if alert["status"] == "resolved":
                status = INCIDENT_STATUS['RESOLVED']
            if alert["status"] == "firing":
                status = INCIDENT_STATUS['FIRING']

            # severity is 0 if warning and 1 if critical
            severity = INCIDENT_SEVERITY['UNKNOWN'] 
            if alert["labels"]["severity"] == "warning":
                severity = INCIDENT_SEVERITY['WARNING'] 
            if alert["labels"]["severity"] == "critical":
                severity = INCIDENT_SEVERITY['CRITICAL']

            startsAt = timezone.make_aware(datetime.datetime.strptime(alert["startsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

            # WE RECEIVE AN UPDATE ABOUT AN INSTANCE DOWN EVENT
            if alert["labels"]["alertname"] == "InstanceDown":

                if severity == INCIDENT_SEVERITY['CRITICAL']:
                    startsAt = startsAt - timedelta(minutes=settings.IS_SERVICE_DOWN_TRIGGER_OUTRAGE_MINUTES)

                service = None
                if alert["labels"]["service"]:
                    service = Service.objects.get(pk=alert["labels"]["service"])

                endsAt = None

                # If there is an endsAt,it means we received a status RESOLVED event
                if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
                    endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

                ignore_warning_resolved = False

                # If we receive a wanring resolve
                if status == INCIDENT_STATUS['RESOLVED'] and severity == INCIDENT_SEVERITY['WARNING'] :
                    # If there is a critical at the same time, we ignore warning resolve
                    if InstanceDownIncident.objects.filter(startsAt=startsAt, severity=INCIDENT_SEVERITY['CRITICAL'], service=service):
                        ignore_warning_resolved = True

                # If we receive resolved, we delete firing with same startAt and fingerprint
                try:
                    # We might receive multiple critical event as every 12h alertmanager repeat the critical event. 
                    # This is about deleting all copy.
                    if status == INCIDENT_STATUS['RESOLVED'] or status == INCIDENT_STATUS['FIRING']:
                        items = InstanceDownIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=INCIDENT_STATUS['FIRING'])
                        for item in items:
                            item.delete()
                except:
                    pass

                if not ignore_warning_resolved:
                    object = InstanceDownIncident(
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
                    object.save()
            elif "project" in alert["labels"]:
                project = None
                if alert["labels"]["project"]:
                    project = Project.objects.get(pk=alert["labels"]["project"])

                endsAt = None
                if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
                    endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

                # If we receive resolved, we delete firing with same startAt and fingerprint
                try:
                    if status == INCIDENT_STATUS['RESOLVED'] or status == INCIDENT_STATUS['FIRING']:
                        items = ProjectIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=INCIDENT_STATUS['FIRING'])
                        for item in items:
                            item.delete()
                except:
                    pass

                object = ProjectIncident(
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
                object.save()
            else:
                endsAt = None
                if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
                    endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

                # If we receive resolved, we delete firing with same startAt and fingerprint
                try:
                    if status == INCIDENT_STATUS['RESOLVED'] or status == INCIDENT_STATUS['FIRING']:
                        items = GenericIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=INCIDENT_STATUS['FIRING'])
                        for item in items:
                            startsAt = item.startsAt
                            item.delete()
                except:
                    pass

                object = GenericIncident(
                    startsAt=startsAt,
                    endsAt=endsAt,
                    fingerprint=alert["fingerprint"],
                    instance=alert["labels"]["instance"] if 'instance' in alert["labels"] else None,
                    summary=alert["annotations"]["summary"],
                    description=alert["annotations"]["description"],
                    severity=severity,
                    status=status,
                    json=json_formated)
                object.save()

    return Response()
