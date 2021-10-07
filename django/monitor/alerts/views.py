from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import GenericAlert, InstanceDownAlert, ApplicationAlert
from applications.models import Service, Application

import json
import datetime
# Create your views here.

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
                        items = InstanceDownAlert.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=2)
                        for item in items:
                            item.delete()
                except:
                    pass

                object = InstanceDownAlert(
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
            elif "application" in alert["labels"]:
                application = None
                if alert["labels"]["application"]:
                    application = Application.objects.get(pk=alert["labels"]["application"])

                endsAt = None
                if alert["endsAt"] and not alert["endsAt"].startswith("0001"):
                    endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

                # If we receive resolved, we delete firing with same startAt and fingerprint
                try:
                    if alert["status"] == "resolved":
                        items = ApplicationAlert.objects.filter(fingerprint=alert["fingerprint"], startsAt=startsAt, status=2)
                        for item in items:
                            item.delete()
                except:
                    pass

                object = ApplicationAlert(
                    application=application,
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
                        items = GenericAlert.objects.filter(fingerprint=alert["fingerprint"], status=2)
                        for item in items:
                            startsAt = item.startsAt
                            item.delete()
                except:
                    pass

                object = GenericAlert(
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
