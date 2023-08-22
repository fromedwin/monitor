from django.shortcuts import render, redirect

from django.urls import reverse

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Emails
from .forms import EmailsForm
from projects.models import Project
from incidents.models import ServiceIncident

from django.conf import settings

@login_required
def project_notifications(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    service_incidents = ServiceIncident\
        .objects\
        .filter(service__project=project, incident__ends_at__isnull=False)\
        .order_by('-incident__starts_at', '-incident__severity')[:40]

    # Group incidents per date based on day month and year
    dates = {}
    for service_incident in service_incidents:
        if service_incident.incident.starts_at.date() in dates:
            dates[service_incident.incident.starts_at.date()].append(service_incident)
        else:
            dates[service_incident.incident.starts_at.date()] = [service_incident]

    return render(request, 'project/notifications.html', {
        'project': project,
        'dates': dates,
    })

@login_required
def email_form(request, application_id, email_id=None):

    email = None

    if email_id != None:
        email = get_object_or_404(Emails, pk=email_id)
        project = email.project
    else:
        project = get_object_or_404(Project, pk=application_id)

    if request.POST:

        form = EmailsForm(request.POST, instance=email)

        if form.is_valid():
            email = form.save(commit=False)
            email.project = project
            email.save()

            return redirect(reverse('project_notifications', args=[application_id]))
    else:
        if email:
            form = EmailsForm(instance=email)
        else:
            form = EmailsForm()

    return render(request, 'notifications/emails/form.html', {
        'project': project,
        'email': email,
        'form': form,
    })

@login_required
def email_delete(request, application_id, email_id):

    email = get_object_or_404(Emails, pk=email_id)
    email.delete()

    return redirect(reverse('project_notifications', args=[application_id]))

@login_required
def messages(request):

    # If user has no project we redirect to /welcome/
    if not request.user.projects.all():
        return redirect('projects_welcome')

    service_incidents = ServiceIncident\
        .objects\
        .filter(service__project__in=request.user.projects.all(), incident__ends_at__isnull=False)\
        .order_by('-incident__starts_at', '-incident__severity')[:40]

    # Group incidents per date based on day month and year
    dates = {}
    for service_incident in service_incidents:
        if service_incident.incident.starts_at.date() in dates:
            dates[service_incident.incident.starts_at.date()].append(service_incident)
        else:
            dates[service_incident.incident.starts_at.date()] = [service_incident]

    return render(request, 'chat.html', {
        'settings': settings,
        'dates': dates,
    })
