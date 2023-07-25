from django.shortcuts import render, redirect

from django.urls import reverse

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Pager_Duty, Emails
from .forms import PagerDutyForm, EmailsForm
from projects.models import Project

@login_required
def project_notifications(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'project/notifications.html', {
        'project': project,
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
def pagerduty_form(request, application_id, pagerduty_id=None):

    pagerduty = None

    if pagerduty_id != None:
        pagerduty = get_object_or_404(Pager_Duty, pk=pagerduty_id)
        project = pagerduty.project
    else:
        project = get_object_or_404(Project, pk=application_id)

    if request.POST:

        form = PagerDutyForm(request.POST, instance=pagerduty)

        if form.is_valid():
            pagerduty = form.save(commit=False)
            pagerduty.project = project
            pagerduty.save()

            return redirect(reverse('project_notifications', args=[application_id]))
    else:
        if pagerduty:
            form = PagerDutyForm(instance=pagerduty)
        else:
            form = PagerDutyForm()

    return render(request, 'notifications/pagerduty/form.html', {
        'project': project,
        'pagerduty': pagerduty,
        'form': form,
    })

@login_required
def pagerduty_delete(request, application_id, pagerduty_id):

    pagerduty = get_object_or_404(Pager_Duty, pk=pagerduty_id)
    pagerduty.delete()

    return redirect(reverse('project_notifications', args=[application_id]))
