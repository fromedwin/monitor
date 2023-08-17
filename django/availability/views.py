import requests
import json
import datetime

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialApp

from workers.models import Server
from incidents.models import ServiceIncident
from projects.models import Project
from projects.forms import ProjectForm

from .models import Service, HTTPCodeService, HTTPMockedCodeService
from .forms import ServiceForm, HTTPCodeServiceForm, MockedHTTPCodeServiceForm



HEADERS = {
    'User-Agent': 'FromEdwinBot Python Django',
}


@login_required
def project_availability(request, id):
    """
    Show current project status
    """
    duration = 60*60
    if 'duration' in request.GET:
        duration = int(request.GET['duration'])

    # Set a max value for duration to save some performance issues on backend
    if duration > 604800:
        duration = 604800


    project = get_object_or_404(Project, pk=id)

    number_days = 30

    start_date = timezone.now() - timezone.timedelta(days=number_days)
    incidents = ServiceIncident.objects.filter(service__project=project, startsAt__gte=start_date, severity=2)

    days = []
    for day in reversed(range(number_days)):
        day = timezone.now() - timezone.timedelta(days=day)
        start_of_day = timezone.datetime(day.year,day.month,day.day)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        days.append({
            'day': start_of_day,
            'outrage': ServiceIncident.objects.filter(
                service__project = project, 
                incident__severity = 2,
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
            'degradated': ServiceIncident.objects.filter(
                service__project = project, 
                incident__severity = 2, 
                service__is_critical = False).filter(
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

    content = {}
    services = {}
    graph = []

    try:
        servers = Server.objects.filter(
            monitoring=True,
            last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
        ).order_by('-last_seen')

        server = servers[0]
        authbasic = server.authbasic.first()

        """
            Fetch prometheus probe duration seconds data
        """
        response = requests.get(f'{server.href}/fastapi/availability/{id}?duration={duration}', headers=HEADERS, auth=(authbasic.username, authbasic.password))
        response.raise_for_status()
        content = json.loads(response.content)

        services = content['services']

        for service in services:
            try:
                services[service]['title'] = Service.objects.get(id=service).title
            except:
                # Remove data from availability is Service no longer exist (jsut deleted use case)
                services = {k: v for k, v in services.items() if k != service}

    except Exception as err:
        content = {
            'error': getattr(err, 'message', repr(err))
        }

    return render(request, 'project/availability.html', {
        'project': project,
        'incidents': incidents,
        'days': days,
        'settings': settings,
        'services': services,
        'duration': duration,
        'availability': {
            '1': project.availability(days=1),
            '7': project.availability(days=7),
            '30': project.availability(days=30),
        },
        'url': f'{request.META["wsgi.url_scheme"]}://{request.META["HTTP_HOST"]}',
    })

@login_required
def service_list(request, application_id):
    """
    List of services
    """
    return render(request, 'project/services/service_list.html', {'application_id': application_id})

@login_required
def service_http_form(request, application_id, service_http_id=None):
    """
        Create or edit service model
    """

    service_http = None

    if service_http_id != None:
        service_http = get_object_or_404(HTTPCodeService, pk=service_http_id)
        project = service_http.service.project
    else:
        project = get_object_or_404(Project, pk=application_id)

    if request.POST:

        form = HTTPCodeServiceForm(request.POST, instance=service_http, project=project)
        if service_http:
            formService = ServiceForm(request.POST, instance=service_http.service)
        else:
            formService = ServiceForm(request.POST)

        if form.is_valid() and formService.is_valid():

            service = formService.save(commit=False)
            service.project = project
            service.save()

            service_http = form.save(commit=False)
            service_http.service = service
            service_http.save()

            return redirect(reverse('project_availability', args=[application_id]))
    else:
        if service_http and service_http.service:
            form = HTTPCodeServiceForm(instance=service_http)
            formService = ServiceForm(instance=service_http.service)
        else:
            form = HTTPCodeServiceForm()
            formService = ServiceForm()

    return render(request, 'project/services/httpcode/httpcode_form.html', {
        'project': project,
        'service_http': service_http,
        'form': form,
        'formService': formService,
    })

@login_required
def service_http_delete(request, application_id, service_http_id):
    """
        Delete service model
    """

    service = get_object_or_404(HTTPCodeService, pk=service_http_id)
    service.service.delete()

    return redirect(reverse('project_availability', args=[application_id]))

@login_required
def service_mockedhttp_form(request, application_id, service_http_id=None):
    """
        Create or edit service model
    """

    service_http = None

    if service_http_id != None:
        service_http = get_object_or_404(HTTPMockedCodeService, pk=service_http_id)
        project = service_http.service.project
    else:
        project = get_object_or_404(Project, pk=application_id)

    if request.POST:

        form = MockedHTTPCodeServiceForm(request.POST, instance=service_http)
        if service_http:
            formService = ServiceForm(request.POST, instance=service_http.service)
        else:
            formService = ServiceForm(request.POST)

        if form.is_valid() and formService.is_valid():

            service = formService.save(commit=False)
            service.project = project
            service.save()

            service_http = form.save(commit=False)
            service_http.service = service
            service_http.save()

            return redirect(reverse('project_availability', args=[application_id]))
    else:
        if service_http and service_http.service:
            form = MockedHTTPCodeServiceForm(instance=service_http)
            formService = ServiceForm(instance=service_http.service)
        else:
            form = MockedHTTPCodeServiceForm()
            formService = ServiceForm()

    return render(request, 'project/services/mockedhttpcode/mockedhttpcode_form.html', {
        'project': project,
        'service_http': service_http,
        'form': form,
        'formService': formService,
    })

# Return Mocked HTTP service code with code
def healthy(request, id):
    obj = get_object_or_404(HTTPMockedCodeService, pk=id)
    return HttpResponse(status=obj.code, content=obj.code)

@login_required
def service_mockedhttp_delete(request, application_id, service_http_id):
    """
        Delete service model
    """

    service = get_object_or_404(HTTPMockedCodeService, pk=service_http_id)
    service.service.delete()

    return redirect(reverse('project_availability', args=[application_id]))

@login_required
def availabilities_all(request):
    """
    Show current project status
    """
    id = request.user.id

    content = {}
    services = {}

    try:
        servers = Server.objects.filter(
            monitoring=True,
            last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
        ).order_by('-last_seen')

        server = servers[0]
        authbasic = server.authbasic.first()

        """
            Fetch prometheus probe duration seconds data
        """
        response = requests.get(f'{server.href}/fastapi/availabilities/{id}', headers=HEADERS, auth=(authbasic.username, authbasic.password))
        response.raise_for_status()
        content = json.loads(response.content)

        services = content['services']

        for service in services:
            try:
                services[service]['title'] = Service.objects.get(id=service).title
            except:
                # Remove data from availability is Service no longer exist (jsut deleted use case)
                services = {k: v for k, v in services.items() if k != service}

    except Exception as err:
        content = {
            'error': getattr(err, 'message', repr(err))
        }

    return render(request, 'project/availabilities.html', {
        'projects': request.user.applications.all(),
        'settings': settings,
        'services': services,
        'url': f'{request.META["wsgi.url_scheme"]}://{request.META["HTTP_HOST"]}',
    })
