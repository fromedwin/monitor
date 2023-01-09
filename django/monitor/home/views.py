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

from clients.models import Server
from incidents.models import GenericIncident, InstanceDownIncident, ProjectIncident

def index(request):
    """
    Home page return dashboard view if loggedin, or welcome page if anonymous.
    """

    if request.user.is_anonymous:

        socialapps = SocialApp.objects.all()
        return render(request, 'homepage.html', {
            'socialapps': socialapps,
        })

    activities = InstanceDownIncident.objects.filter(service__project__in=request.user.applications.all()).order_by('-creation_date')[:20]

    return render(request, 'dashboard.html', {
        'settings': settings,
        'activities': activities
    })

