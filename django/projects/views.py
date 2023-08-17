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
from incidents.models import ServiceIncident

from performances.models import Performance

@login_required
def project(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    incidents = ServiceIncident\
        .objects\
        .filter(
            service__project = project, 
            incident__ends_at__isnull = False)\
        .order_by('-ends_at', '-severity')[:5]

            # Group incidents per date based on day month and year
    dates = {}
    for incident in incidents:
        if incident.ends_at.date() in dates:
            dates[incident.ends_at.date()].append(incident)
        else:
            dates[incident.ends_at.date()] = [incident]

    return render(request, 'projects/project_view.html', {
        'project': project,
        'settings': settings,
        'dates': dates,
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
        form = ProjectCreateForm(request.POST, user=request.user)

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

        form = ProjectCreateForm(request.POST, user=request.user)

        if form.is_valid():
            project = form.save(user=request.user)
            return redirect(reverse('project', args=[project.id]))
    else:
        form = ProjectCreateForm()

    return render(request, 'projects/project_welcome.html', {
        'form': form,
    })

