import requests
import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from projects.models import Project
from .models import Performance
from .forms import PerformanceForm

@login_required
def project_performances(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'project/performances.html', {
        'project': project,
    })


@login_required
def performance_form(request, application_id, performance_id=None):
    """
        Create or edit service model
    """

    performance = None

    if performance_id != None:
        performance = get_object_or_404(Performance, pk=performance_id)
        project = performance.project
    else:
        project = get_object_or_404(Project, pk=application_id)

    if request.POST:

        form = PerformanceForm(request.POST, instance=performance)

        if form.is_valid():

            performance = form.save(commit=False)
            performance.project = project
            performance.save()

            return redirect(reverse('project_performances', args=[application_id]))
    else:
        if performance:
            form = PerformanceForm(instance=performance)
        else:
            form = PerformanceForm()

    return render(request, 'project/performances/performances_form.html', {
        'project': project,
        'performance': performance,
        'form': form,
    })

@login_required
def performance_delete(request, server_id, performance_id):
    """
        Delete service model
    """

    performance = get_object_or_404(Performance, pk=performance_id)
    performance.delete()

    return redirect(reverse('project_performances', args=[application_id]))
