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

            startsAt = timezone.make_aware(datetime.datetime.strptime(alert["startsAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=settings.IS_SERVICE_DOWN_TRIGGER_OUTRAGE_MINUTES))

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

@login_required
def incidents(request, id, year=None, month=None, day=None):
    """
    List of incidents for a specific projects
    """
    project = get_object_or_404(Project, pk=id)

    if year and month and day:
        number_days = 1
        now = timezone.datetime(year, month, day)
        date = now
    else:
        number_days = 30
        now = timezone.now()
        date = None

    days = []
    for day in range(number_days):
        day = now - timezone.timedelta(days=day)
        start_of_day = timezone.datetime(day.year,day.month,day.day)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        days.append({
            'day': start_of_day,
            'incidents': InstanceDownIncident.objects.filter(service__project=project, severity=2).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)).order_by('startsAt'),
            'outrage': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_critical=True).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
            'degradated': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_critical=False).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
        })

    return render(request, 'incidents.html', {
        'project': project,
        'days': days,
        'date': date,
    })