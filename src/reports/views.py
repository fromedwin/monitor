from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from .models import ProjectReport

@login_required
def project_reports(request, id):
    """Project-specific reports page"""
    project = get_object_or_404(Project, id=id, user=request.user)
    
    # Get all reports for this project
    reports = project.project_report.all().order_by('-creation_date')
    
    context = {
        'project': project,
        'reports': reports,
    }
    return render(request, 'reports/project_reports.html', context)

@login_required
def report_email_preview(request, project_id, report_id):
    """Preview the email template for a specific report"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    report = get_object_or_404(ProjectReport, id=report_id, project=project)
    
    # Create the report URL for the email template
    from django.conf import settings
    report_url = f"{getattr(settings, 'BACKEND_URL', 'http://localhost:8000')}/project/{project.id}/reports/"
    
    context = {
        'project': project,
        'report': report,
        'report_url': report_url,
        'user': request.user,
    }
    return render(request, 'reports/emails/report_available.html', context)
