import requests
import json
from pathlib import Path
from django.urls import reverse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.decorators.cache import never_cache

from constants import INCIDENT_SEVERITY
from incidents.models import Incident
from projects.models import Project

from django.http import Http404

@login_required
def toggle_public_page(request, application_id):
    project = get_object_or_404(Project, pk=application_id)

    if request.POST:
        project.enable_public_page = not project.enable_public_page
        project.save()
        return redirect(reverse('project_status_public', args=[project.id]))
    else:
        redirect(reverse('project_status_public', args=[project.id]))


@login_required
def project_status_public(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'project/status_public.html', {
        'project': project,
    })


@never_cache
def badge(request, id):
    """
    Show Public view of a project status
    """

    project = get_object_or_404(Project, pk=id)

    if not project.enable_public_page:
        raise Http404()

    if project.is_offline():
        file = 'badge-offline.svg'
    elif project.is_degraded():
        file = 'badge-degraded.svg'
    elif project.is_warning():
        file = 'badge-degraded.svg'
    else:
        file = 'badge-online.svg'
    
    # path will look like /this/project/path/monitor/fromedwin
    path = str(Path(__file__).resolve().parent) 
    image_data = open(f'{path}/static/badges/{file}', mode='r').read()

    return HttpResponse(image_data, content_type="image/svg+xml")

def public(request, id):
    """
    Show Public view of a project status
    """

    project = get_object_or_404(Project, pk=id)

    # Return 404 if user did not enable public status page
    if not project.enable_public_page:
        raise Http404()

    # We display 30 days
    NUMBER_DAYS = 30

    start_date = timezone.now() - timezone.timedelta(days=NUMBER_DAYS)
    incidents = Incident.objects.filter(
        service__project = project, 
        starts_at__gte = start_date, 
        severity = 2
    )

    days = []
    for day in range(NUMBER_DAYS):
        day = timezone.now() - timezone.timedelta(days=day)
        start_of_day = timezone.datetime(day.year,day.month,day.day)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        days.append({
            'day': start_of_day,
            'incidents': Incident.objects.filter(service__project=project, severity=INCIDENT_SEVERITY['CRITICAL'], service__is_enabled=True).filter(Q(starts_at__gte=start_of_day, ends_at__lt=end_of_day)|Q(starts_at__lt=start_of_day, ends_at__gt=start_of_day)|Q(starts_at__lt=end_of_day, ends_at__gt=end_of_day)).order_by('starts_at'),
            'outrage': Incident.objects.filter(service__project=project, severity=INCIDENT_SEVERITY['CRITICAL'], service__is_enabled=True, service__is_critical=True).filter(Q(starts_at__gte=start_of_day, ends_at__lt=end_of_day)|Q(starts_at__lt=start_of_day, ends_at__gt=start_of_day)|Q(starts_at__lt=end_of_day, ends_at__gt=end_of_day)),
            'degradated': Incident.objects.filter(service__project=project, severity=INCIDENT_SEVERITY['CRITICAL'], service__is_enabled=True, service__is_critical=False).filter(Q(starts_at__gte=start_of_day, ends_at__lt=end_of_day)|Q(starts_at__lt=start_of_day, ends_at__gt=start_of_day)|Q(starts_at__lt=end_of_day, ends_at__gt=end_of_day)),
        })

    return render(request, 'public.html', {
        'project': project,
        'services': project.services.filter(is_public=True, is_enabled=True),
        'incidents': incidents,
        'availability': {
            '1': project.availability(days=1),
            '7': project.availability(days=7),
            '30': project.availability(days=30),
        },
        'days': days,
        'days_reverses': reversed(days),
    })
