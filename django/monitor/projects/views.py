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
from projects.models import Project, Service
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from projects.forms import ProjectForm, ServiceForm

@login_required
def projects(request):
    """
    List of projects for current user
    """
    return render(request, 'projects/project_list.html', {})

@login_required
def project(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'projects/project_view.html', {
        'project': project
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

@login_required
def service_form(request, application_id, service_id=None):
    """
        Create or edit service model
    """

    service = None

    if service_id != None:
        service = get_object_or_404(Service, pk=service_id)
        project = service.project
    else:
        project = get_object_or_404(Project, pk=application_id)

    if request.POST:

        form = ServiceForm(request.POST, instance=service)

        if form.is_valid():
            service = form.save(commit=False)
            service.project = project
            service.save()

            return redirect(reverse('project', args=[application_id]))
    else:
        if service:
            form = ServiceForm(instance=service)
        else:
            form = ServiceForm()

    return render(request, 'projects/services/service_form.html', {
        'project': project,
        'service': service,
        'form': form,
    })

@login_required
def service_delete(request, application_id, service_id):
    """
        Delete service model
    """

    service = get_object_or_404(Service, pk=service_id)
    service.delete()

    return redirect(reverse('project', args=[application_id]))