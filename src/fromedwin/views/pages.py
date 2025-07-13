import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from projects.models import Project
from fromedwin.decorators import waiting_list_approved_only

@login_required
@waiting_list_approved_only()
def project_pages(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'pages/pages.html', {
        'project': project,
        'pages_count': project.pages.count(),
        'pages': project.pages.all().order_by('url')
    })
