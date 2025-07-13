import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from projects.models import Project
from fromedwin.decorators import waiting_list_approved_only
from lighthouse.models import LighthouseReport
# Create your views here.

@login_required
@waiting_list_approved_only()
def project_performances_report_viewer(request, id, report_id):
    """
    Show current project status
    """
    
    project = get_object_or_404(Project, pk=id)

    report = get_object_or_404(LighthouseReport, pk=report_id)
    report_json = json.loads(report.report_json_file.read())

    return render(request, 'lighthouse-viewer.html', {
        'project': project,
        'report': report,
        'json': json.dumps(report_json),
    })
