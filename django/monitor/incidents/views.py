import json
import datetime
from django.shortcuts import render
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GenericIncident, InstanceDownIncident, ProjectIncident
from projects.models import Project, Service

@api_view(["POST"])
def webhook(request):
    if request.data["alerts"]:
        for alert in request.data["alerts"]:
            json_formated = json.dumps(alert, indent=2, sort_keys=True)

            # Status is 0 if resolved and 1 if firing
            status = 0
            if alert["status"] == "resolved":
                status = 1
            if alert["status"] == "firing":
                status = 2

            # severity is 0 if warning and 1 if critical
            severity = 0
            if alert["labels"]["severity"] == "warning":
                severity = 1
            if alert["labels"]["severity"] == "critical":
                severity = 2

            startsAt = timezone.make_aware(datetime.datetime.strptime(alert["startsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

            if alert["labels"]["alertname"] == "InstanceDown":

                service = None
                if alert["labels"]["service"]:
                    service = Service.objects.get(pk=alert["labels"]["service"])

                endsAt = None
                if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
                    endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

                # If we receive resolved, we delete firing with same startAt and fingerprint
                try:
                    if alert["status"] == "resolved":
                        items = InstanceDownIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=2)
                        for item in items:
                            item.delete()
                except:
                    pass

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
                    if alert["status"] == "resolved":
                        items = ProjectIncident.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=2)
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
                    if alert["status"] == "resolved":
                        items = GenericIncident.objects.filter(fingerprint=alert["fingerprint"], status=2)
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