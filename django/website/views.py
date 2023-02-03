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

def homepage(request):
    """
    Home Welcome page
    """
    socialapps = SocialApp.objects.all()

    return render(request, 'homepage.html', {
        'socialapps': socialapps,
        'is_authenticated': request.user.is_authenticated
    })
