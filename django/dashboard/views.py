import datetime

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from allauth.socialaccount.models import SocialApp
from rest_framework.authtoken.models import Token

from workers.models import Server
from alerts.models import GenericIncident, InstanceDownIncident, ProjectIncident

@login_required
def dashboard(request):

    # If user has no project we redirect to /welcome/
    if not request.user.applications.all():
        return redirect('projects_welcome')

    incidents = InstanceDownIncident\
        .objects\
        .filter(service__project__in=request.user.applications.all(), endsAt__isnull=False)\
        .order_by('-startsAt', '-severity')[:20]

    # Group incidents per date based on day month and year
    dates = {}
    for incident in incidents:
        if incident.startsAt.date() in dates:
            dates[incident.startsAt.date()].append(incident)
        else:
            dates[incident.startsAt.date()] = [incident]

    return render(request, 'dashboard.html', {
        'settings': settings,
        'dates': dates,
    })
