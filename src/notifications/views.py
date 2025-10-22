from django.shortcuts import render, redirect

from django.urls import reverse

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Notification, Emails
from .forms import EmailsForm
from projects.models import Project
from incidents.models import Incident

from fromedwin.decorators import waiting_list_approved_only
from django.conf import settings

@login_required
@waiting_list_approved_only()
def project_notifications(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    notifications = Notification.objects.filter(service__project=project)\
        .order_by('-date')[:40]

    # Group incidents per date based on day month and year
    dates = {}
    for notification in notifications:
        if notification.date.date() in dates:
            dates[notification.date.date()].append(notification)
        else:
            dates[notification.date.date()] = [notification]

    return render(request, 'project/notifications.html', {
        'project': project,
        'dates': dates,
    })

@login_required
@waiting_list_approved_only()
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
@waiting_list_approved_only()
def email_delete(request, application_id, email_id):

    email = get_object_or_404(Emails, pk=email_id)
    email.delete()

    return redirect(reverse('project_notifications', args=[application_id]))

@login_required
@waiting_list_approved_only()
def messages(request):

    notifications = Notification.objects.filter(service__project__in=request.user.projects.all())\
        .order_by('-date')[:40]

    # Group incidents per date based on day month and year
    dates = {}
    for notification in notifications:
        if notification.date.date() in dates:
            dates[notification.date.date()].append(notification)
        else:
            dates[notification.date.date()] = [notification]

    return render(request, 'chat.html', {
        'settings': settings,
        'dates': dates,
    })
