import requests
import json
import datetime

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateformat import format
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialApp

from .forms import ProjectForm, ProjectCreateForm

from projects.models import Project
from availability.models import Service, HTTPCodeService, HTTPMockedCodeService
from workers.models import Server
from alerts.models import InstanceDownIncident
from availability.forms import ServiceForm, HTTPCodeServiceForm, MockedHTTPCodeServiceForm

from performances.models import Performance

@login_required
def project(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    activities = InstanceDownIncident\
        .objects\
        .filter(service__project=project, endsAt__isnull=False)\
        .order_by('-startsAt', '-severity')[:20]

    # Check last ping date
    last_check = None

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
            values = service['values']
            """
                {'metric': 
                    {'__name__': 'probe_duration_seconds', 
                    'application': '50', 
                    'instance': 'https://sebastienbarbier.com', 
                    'job': 'is_service_down', 
                    'service': '53'}, 
                'values': [
                    [1679226664, '0.228248501'], 
                    [1679226694, '0.162575'], 
                    ...
                    [1679227234, '0.191770291'], 
                    [1679227264, '0.191770291']]}
            """
            last_service_check = datetime.datetime.fromtimestamp(int(values[len(values)-1][0]))
            # if last_check is None or last_check > last_service_check:
            #     last_check = last_service_check
            #     print(last_check)
    except:
        pass

    return render(request, 'projects/project_view.html', {
        'project': project,
        'last_check': last_check,
        'activities': activities,
    })

@login_required
def project_performances(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'projects/performances/performances.html', {
        'project': project,
    })

@login_required
def projects_form(request, id=None):
    """
        Create or edit project model
    """

    application = None
    if id != None:
        application = get_object_or_404(Project, pk=id)

    if request.POST:

        form = ProjectForm(request.POST, instance=application)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            return redirect(reverse('project', args=[project.id]))
    else:
        if application:
            form = ProjectForm(instance=application)
        else:
            form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'application': application,
        'form': form,
    })

@login_required
def projects_delete(request, id=None):
    """
        Delete project model
    """
    project = get_object_or_404(Project, pk=id)
    project.delete()

    return redirect(reverse('dashboard'))
    
@login_required
def projects_add(request):
    """
        Create or edit project model
    """

    if request.POST:

        form = ProjectCreateForm(request.POST)

        if form.is_valid():
            project = form.save(user=request.user)
            return redirect(reverse('project', args=[project.id]))
    else:
        form = ProjectCreateForm()

    return render(request, 'projects/project_add.html', {
        'form': form,
    })

@login_required
def projects_welcome(request):
    """
        Create or edit project model
    """

    if request.POST:

        form = ProjectCreateForm(request.POST)

        if form.is_valid():
            project = form.save(user=request.user)
            return redirect(reverse('project', args=[project.id]))
    else:
        form = ProjectCreateForm()

    return render(request, 'projects/project_welcome.html', {
        'form': form,
    })

