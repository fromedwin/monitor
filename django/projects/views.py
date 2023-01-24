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

from projects.models import Project
from availability.models import Service, HTTPCodeService, HTTPMockedCodeService
from workers.models import Server
from alerts.models import InstanceDownIncident
from projects.forms import ProjectForm
from availability.forms import ServiceForm, HTTPCodeServiceForm, MockedHTTPCodeServiceForm

@login_required
def projects(request):
    """
    List of projects for current user
    """

    applications = request.user.applications.order_by('-is_favorite')

    return render(request, 'projects/project_list.html', {
        'applications': applications
    })

@login_required
def project(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'projects/project_view.html', {
        'project': project,
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

    return redirect(reverse('projects'))
    
