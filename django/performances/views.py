import requests
import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from projects.models import Project

@login_required
def project_performances(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    return render(request, 'project/performances.html', {
        'project': project,
    })

