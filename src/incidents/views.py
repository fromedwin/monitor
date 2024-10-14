import json
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

from core.decorators import waiting_list_approved_only
from .models import Incident
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_SEVERITY, INCIDENT_STATUS

@login_required
@waiting_list_approved_only()
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
            'incidents': Incident.objects.filter(
                service__project = project, 
                severity = INCIDENT_SEVERITY['CRITICAL'],
                service__is_critical = True).filter(
                Q(
                    starts_at__gte = start_of_day, 
                    ends_at__lt = end_of_day) | 
                Q(
                    starts_at__lt = start_of_day, 
                    ends_at__gt = start_of_day) | 
                Q(
                    starts_at__lt = end_of_day, 
                    ends_at__gt = end_of_day)
            ).order_by('starts_at'),
            'outrage': Incident.objects.filter(
                service__project = project, 
                severity = INCIDENT_SEVERITY['CRITICAL'],
                service__is_critical = True).filter(
                Q(
                    starts_at__gte = start_of_day, 
                    ends_at__lt = end_of_day)|
                Q(
                    starts_at__lt = start_of_day, 
                    ends_at__gt = start_of_day)|
                Q(
                    starts_at__lt = end_of_day, 
                    ends_at__gt = end_of_day)
                ),
            'degradated': Incident.objects.filter(
                service__project = project, 
                severity = INCIDENT_SEVERITY['CRITICAL'],
                service__is_critical = True).filter(
                Q(
                    starts_at__gte = start_of_day, 
                    ends_at__lt = end_of_day)|
                Q(
                    starts_at__lt = start_of_day, 
                    ends_at__gt = start_of_day)|
                Q(
                    starts_at__lt = end_of_day, 
                    ends_at__gt = end_of_day)
                ),
        })

    return render(request, 'incidents.html', {
        'project': project,
        'days': days,
        'date': date,
    })


@login_required
@waiting_list_approved_only()
def incidents_force_online(request, service_id):

    service = get_object_or_404(Service, pk=service_id)

    # IF service.project.user is not same as request.use we return not authorized HTTP code
    if service.project.user != request.user:
        return HttpResponse(status=403)

    incidents = Incident.objects.filter(service=service, status=INCIDENT_STATUS['FIRING'])
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
