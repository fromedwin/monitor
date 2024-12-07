import requests
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.safestring import SafeString

from projects.models import Project
from .models import Lighthouse, Report
from core.decorators import waiting_list_approved_only

@login_required
@waiting_list_approved_only()
def project_performances(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'project/performances.html', {
        'project': project,
        'pages_count': project.pages.count(),
        'pages': project.pages.all().order_by('url')
    })

@login_required
@waiting_list_approved_only()
def performance_rerun(request, application_id, performance_id):
    """
        Delete service model
    """

    performance = get_object_or_404(Lighthouse, pk=performance_id)
    performance.request_run = True
    performance.save()

    return redirect(reverse('project_performances', args=[application_id])+'#noanimations')

@login_required
@waiting_list_approved_only()
def project_performances_report_viewer(request, id, report_id):
    """
    Show current project status
    """
    
    project = get_object_or_404(Project, pk=id)

    report = get_object_or_404(Report, pk=report_id)
    report_json = json.loads(report.report_json_file.read())

    return render(request, 'lighthouse-viewer.html', {
        'project': project,
        'report': report,
        'json': json.dumps(report_json),
    })
