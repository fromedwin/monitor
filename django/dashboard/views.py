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
from incidents.models import Incident

@login_required
def dashboard(request):

    # If user has no project we redirect to /welcome/
    if not request.user.projects.all():
        return redirect('projects_welcome')

    service_incidents = Incident\
        .objects\
        .filter(
            service__project__in = request.user.projects.all(), 
            ends_at__isnull = False)\
        .order_by('-ends_at', '-severity')[:20]

    # Group incidents per date based on day month and year
    dates = {}
    for service_incident in service_incidents:
        if service_incident.ends_at.date() in dates:
            dates[service_incident.ends_at.date()].append(service_incident)
        else:
            dates[service_incident.ends_at.date()] = [service_incident]

    return render(request, 'dashboard.html', {
        'settings': settings,
        'dates': dates,
    })
