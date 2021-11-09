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
from projects.models import Application, Service
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from projects.forms import ApplicationForm, ServiceForm

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

    application = None
    if id != None:
        application = get_object_or_404(Application, pk=id)

    if request.POST:

        form = ApplicationForm(request.POST, instance=application)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            return redirect(reverse('project', args=[project.id]))
    else:
        if application:
            form = ApplicationForm(instance=application)
        else:
            form = ApplicationForm()
    return render(request, 'projects/form.html', {
        'application': application,
        'form': form,
    })

@login_required
def projects_delete(request, id=None):

    application = get_object_or_404(Application, pk=id)
    application.delete()

    return redirect(reverse('projects'))


@login_required
def service_form(request, application_id, service_id=None):
    
    service = None

    if service_id != None:
        service = get_object_or_404(Service, pk=service_id)
        application = service.application
    else:
        application = get_object_or_404(Application, pk=application_id)

    if request.POST:

        form = ServiceForm(request.POST, instance=service)

        if form.is_valid():
            service = form.save(commit=False)
            service.application = application
            service.save()

            return redirect(reverse('project', args=[application_id]))
    else:
        if service:
            form = ServiceForm(instance=service)
        else:
            form = ServiceForm()

    return render(request, 'projects/services/form.html', {
        'application': application,
        'service': service,
        'form': form,
    })


@login_required
def service_delete(request, application_id, service_id):

    service = get_object_or_404(Service, pk=service_id)
    service.delete()

    return redirect(reverse('project', args=[application_id]))
