import requests
import json
import datetime

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateformat import format
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialApp

from workers.models import Server
from alerts.models import InstanceDownIncident
from projects.models import Project
from projects.forms import ProjectForm

from .models import Service, HTTPCodeService, HTTPMockedCodeService
from .forms import ServiceForm, HTTPCodeServiceForm, MockedHTTPCodeServiceForm

@login_required
def project_availability(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    number_days = 30

    start_date = timezone.now() - timezone.timedelta(days=number_days)
    incidents = InstanceDownIncident.objects.filter(service__project=project, startsAt__gte=start_date, severity=2)

    days = []
    for day in reversed(range(number_days)):
        day = timezone.now() - timezone.timedelta(days=day)
        start_of_day = timezone.datetime(day.year,day.month,day.day)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        days.append({
            'day': start_of_day,
            'outrage': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_critical=True).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
            'degradated': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_critical=False).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
        })

    content = {}
    graph = []
    https = None

    try:
        servers = Server.objects.filter(
            last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
        ).order_by('-last_seen')

        server = servers[0]
        authbasic = server.authbasic.first()

        headers = {
            'User-Agent': 'FromEdwinBot Python Django',
        }

        start = int(format(timezone.now(), 'U'))

        """
            Fetch prometheus probe duration seconds data
        """
        response = requests.get(f'{server.href}/api/v1/query_range?query=probe_duration_seconds%7Bapplication="{id}"%7D&step=30&start={str(start-600)}&end={str(start)}', headers=headers, auth=(authbasic.username, authbasic.password))
        response.raise_for_status()
        content = json.loads(response.content)
        for service in content['data']['result']:
            service['metric']['title'] = Service.objects.get(id=service['metric']['service']).title

        graph = json.dumps(content)
        """
            Fetch prometheus https expiration value
        """
        response = requests.get(f'{server.href}/api/v1/query?query=probe_ssl_earliest_cert_expiry%7Bapplication="{id}"%7D&time={str(start)}', headers=headers, auth=(authbasic.username, authbasic.password))
        response.raise_for_status()
        content = json.loads(response.content)
        https = {}
        for service in content['data']['result']:
            https[service['metric']['service']] = datetime.datetime.fromtimestamp(int(service['value'][1]))

    except Exception as err:
        content = {
            'error': getattr(err, 'message', repr(err))
        }

    return render(request, 'project/availability.html', {
        'project': project,
        'incidents': incidents,
        'days': days,
        'settings': settings,
        'availability': {
            '1': project.availability(days=1),
            '7': project.availability(days=7),
            '30': project.availability(days=30),
        },
        'graph': graph,
        'https': https,
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

        form = HTTPCodeServiceForm(request.POST, instance=service_http)
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
