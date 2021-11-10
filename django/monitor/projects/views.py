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
from projects.models import Project, HTTPCodeService
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from projects.forms import ProjectForm, ServiceForm, HTTPCodeServiceForm

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

            return redirect(reverse('project', args=[application_id]))
    else:
        if service_http and service_http.service:
            form = HTTPCodeServiceForm(instance=service_http)
            formService = ServiceForm(instance=service_http.service)
        else:
            form = HTTPCodeServiceForm()
            formService = ServiceForm()

    return render(request, 'projects/services/service_form.html', {
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

    return redirect(reverse('project', args=[application_id]))