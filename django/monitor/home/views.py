from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

from rest_framework.authtoken.models import Token
from django.shortcuts import render
from clients.models import Server
import datetime
from django.utils import timezone

from allauth.socialaccount.models import SocialApp
from applications.models import Application
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    if request.user.is_anonymous:

        socialapps = SocialApp.objects.all()
        return render(request, 'homepage.html', {
            'socialapps': socialapps,
        })

    token = None
    is_staff = False
    servers = []

    token = Token.objects.get(user=request.user)
    servers = Server.objects.filter(
        last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-last_seen')


    return render(request, 'dashboard.html', {
        'servers': servers,
        'token': token,
        'settings': settings,
    })

@login_required
def projects(request):

    return render(request, 'projects.html', {})


@login_required
def project(request, id):

    application = get_object_or_404(Application, pk=id)

    return render(request, 'project.html', {
        'application': application
    })

@login_required
def projects_form(request, id=None):
    
    if request.POST:
        return redirect(reverse('projects'))

    application = None

    if id != None:
        application = get_object_or_404(Application, pk=id)

    return render(request, 'projects/form.html', {
        'application': application
    })

@login_required
def projects_delete(request, id=None):
    return redirect(reverse('projects'))


@login_required
def service_form(request, application_id, service_id=None):
    
    application = None

    if application_id != None:
        application = get_object_or_404(Application, pk=application_id)

    return render(request, 'projects/services/form.html', {
        'application': application,
        'service': { 'id': service_id },
    })
