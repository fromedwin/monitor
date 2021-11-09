from django.shortcuts import render, redirect

from django.urls import reverse

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Pager_Duty
from .forms import PagerDutyForm
from projects.models import Project

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

            return redirect(reverse('project', args=[application_id]))
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

    return redirect(reverse('project', args=[application_id]))
