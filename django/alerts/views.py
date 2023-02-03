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
from projects.models import Project
from availability.models import Service

from constants import INCIDENT_SEVERITY

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
            'incidents': InstanceDownIncident.objects.filter(service__project=project, severity=INCIDENT_SEVERITY['CRITICAL']).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)).order_by('startsAt'),
            'outrage': InstanceDownIncident.objects.filter(service__project=project, severity=INCIDENT_SEVERITY['CRITICAL'], service__is_critical=True).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
            'degradated': InstanceDownIncident.objects.filter(service__project=project, severity=INCIDENT_SEVERITY['CRITICAL'], service__is_critical=False).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
        })

    return render(request, 'incidents.html', {
        'project': project,
        'days': days,
        'date': date,
    })
