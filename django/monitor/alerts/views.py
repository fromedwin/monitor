from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import GenericAlert, InstanceDownAlert

import json
import datetime
# Create your views here.

@api_view(["POST"])
def webhook(request):
    if request.data["alerts"]:
        for alert in request.data["alerts"]:
            json_formated = json.dumps(alert, indent=2, sort_keys=True)
            if alert["labels"]["alertname"] == "InstanceDown":

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

                endsAt = None
                if  alert["endsAt"] and not alert["endsAt"].startswith("0001"):
                    endsAt = timezone.make_aware(datetime.datetime.strptime(alert["endsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"))

                # If we receive resolved, we delete firing with same startAt and fingerprint
                try:
                    if alert["status"] == "resolved":
                        InstanceDownAlert.objects.get(fingerprint=alert["fingerprint"], startsAt=startsAt, status=2).delete()
                except:
                    pass

                object = InstanceDownAlert(
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
                object = GenericAlert(json=json_formated)
                object.save()
    else:
        json_formated = json.dumps(request.data, indent=2, sort_keys=True)
        object = GenericAlert(json=json_formated, fingerprint="Unknown")
        object.save()

    return Response()
