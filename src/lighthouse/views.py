import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from projects.models import Project
from fromedwin.decorators import waiting_list_approved_only
from lighthouse.models import LighthouseReport

@login_required
@waiting_list_approved_only()
def project_pages_report_viewer(request, id, report_id):
    """
    Show current project status
    """
    
    project = get_object_or_404(Project, pk=id)
    report = get_object_or_404(LighthouseReport, pk=report_id)
    
    return render(request, 'lighthouse-viewer.html', {
        'project': project,
        'report': report,
    })
