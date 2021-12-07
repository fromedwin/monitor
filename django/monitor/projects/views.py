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

from projects.models import Project, HTTPCodeService, HTTPMockedCodeService
from clients.models import Server
from incidents.models import InstanceDownIncident
from projects.forms import ProjectForm, ServiceForm, HTTPCodeServiceForm, MockedHTTPCodeServiceForm

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

    return render(request, 'projects/project_view.html', {
        'project': project,
        'incidents': incidents,
        'days': days,
        'settings': settings
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
def service_list(request, application_id):
    """
    List of services
    """
    return render(request, 'projects/services/service_list.html', {'application_id': application_id})

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

    return render(request, 'projects/services/httpcode/httpcode_form.html', {
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

            return redirect(reverse('project', args=[application_id]))
    else:
        if service_http and service_http.service:
            form = MockedHTTPCodeServiceForm(instance=service_http)
            formService = ServiceForm(instance=service_http.service)
        else:
            form = MockedHTTPCodeServiceForm()
            formService = ServiceForm()

    return render(request, 'projects/services/mockedhttpcode/mockedhttpcode_form.html', {
        'project': project,
        'service_http': service_http,
        'form': form,
        'formService': formService,
    })

@login_required
def service_mockedhttp_delete(request, application_id, service_http_id):
    """
        Delete service model
    """

    service = get_object_or_404(HTTPMockedCodeService, pk=service_http_id)
    service.service.delete()

    return redirect(reverse('project', args=[application_id]))

@login_required
def toggle_public_page(request, application_id):
    project = get_object_or_404(Project, pk=application_id)

    if request.POST:
        project.enable_public_page = not project.enable_public_page
        project.save()
        return redirect(reverse('project', args=[project.id]))
    else:
        redirect(reverse('project', args=[project.id]))