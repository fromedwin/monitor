from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project

# Create your views here.

@login_required
def reports_home(request):
    """Home page for reports showing list of all reports"""
    # Get all projects for the current user
    projects = request.user.projects.all().order_by('title')
    
    context = {
        'projects': projects,
    }
    return render(request, 'reports/reports_home.html', context)

@login_required
def project_reports(request, id):
    """Project-specific reports page"""
    project = get_object_or_404(Project, id=id, user=request.user)
    
    context = {
        'project': project,
    }
    return render(request, 'reports/project_reports.html', context)
