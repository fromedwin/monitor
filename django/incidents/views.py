import json
import datetime
from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ServiceIncident
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_SEVERITY, INCIDENT_STATUS

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
            'incidents': ServiceIncident.objects.filter(
                service__project = project, 
                incident__severity = INCIDENT_SEVERITY['CRITICAL']).filter(
                Q(
                    incident__starts_at__gte = start_of_day, 
                    incident__ends_at__lt = end_of_day) | 
                Q(
                    incident__starts_at__lt = start_of_day, 
                    incident__ends_at__gt = start_of_day) | 
                Q(
                    incident__starts_at__lt = end_of_day, 
                    incident__ends_at__gt = end_of_day)
            ).order_by('incident__starts_at'),
            'outrage': ServiceIncident.objects.filter(
                service__project = project, 
                incident__severity = INCIDENT_SEVERITY['CRITICAL'], 
                alert__is_critical = True).filter(
                Q(
                    incident__starts_at__gte = start_of_day, 
                    incident__ends_at__lt = end_of_day)|
                Q(
                    incident__starts_at__lt = start_of_day, 
                    incident__ends_at__gt = start_of_day)|
                Q(
                    incident__starts_at__lt = end_of_day, 
                    incident__ends_at__gt = end_of_day)
                ),
            'degradated': ServiceIncident.objects.filter(
                service__project = project, 
                incident__severity = INCIDENT_SEVERITY['CRITICAL'], 
                alert__is_critical = False).filter(
                Q(
                    incident__starts_at__gte = start_of_day, 
                    incident__ends_at__lt = end_of_day)|
                Q(
                    incident__starts_at__lt = start_of_day, 
                    incident__ends_at__gt = start_of_day)|
                Q(
                    incident__starts_at__lt = end_of_day, 
                    incident__ends_at__gt = end_of_day)
                ),
        })

    return render(request, 'incidents.html', {
        'project': project,
        'days': days,
        'date': date,
    })


@login_required
def incidents_force_online(request, service_id):

    service = get_object_or_404(Service, pk=service_id)

    # IF service.project.user is not same as request.use we return not authorized HTTP code
    if service.project.user != request.user:
        return HttpResponse(status=403)

    incidents = ServiceIncident.objects.filter(service=service, incident__status=INCIDENT_STATUS['FIRING'])
    for incident in incidents:
        # Check if path contains delete_incidents
        if 'delete_incidents' in request.path:
            incident.delete()
        else:
            incident.status = INCIDENT_STATUS['RESOLVED']
            incident.ends_at = timezone.now()
            incident.save()

    # Redirect to project view
    return redirect('project_availability', id=service.project.id)
