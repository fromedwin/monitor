import requests
import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.safestring import SafeString

from projects.models import Project
from .models import Performance, Report
from .forms import PerformanceForm

@login_required
def project_performances(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    domains = {} # List of all domains

    # For each performance object we extract the url and index by domain 
    for performance in project.performances.all().order_by('url'):
        
        # Extract domain from url
        domain = performance.url.split('/')[2]

        # if new domain, we create a default object
        if not domains.get(domain):
            domains[domain] = {
                'url': domain,
                'tree': []
            }

        # Recursive function parsing all pages at that level looking if it starts with path
        # If yes it run on children array
        # If none we create a new page at that level
        def find_page(pages, performance, depth=0):
            # print('FIND_PAGE', pages, performance)
            path = '/'.join(performance.url.split('/')[3:])

            if path is not '': #For root url we add directly
                for page in pages:
                    page_path = '/'.join(page['performance'].url.split('/')[3:])
                    # If root url is in pages, we go to children level directly
                    if page_path is '':
                        find_page(page['children'], performance, depth+1)
                        return
                    else:
                        if path.startswith(page_path):
                            if path != page_path:
                                find_page(page['children'], performance, depth+1)
                            return

            pages.append({
                'performance': performance,
                'path': path,
                'depth': depth,
                'children': [],
            })

        # We start with the root page
        find_page(domains[domain]['tree'], performance)


    return render(request, 'project/performances.html', {
        'project': project,
        'domains': domains,
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
def performance_delete(request, application_id, performance_id):
    """
        Delete service model
    """

    performance = get_object_or_404(Performance, pk=performance_id)
    performance.delete()

    return redirect(reverse('project_performances', args=[application_id]))

@login_required
def performance_rerun(request, application_id, performance_id):
    """
        Delete service model
    """

    performance = get_object_or_404(Performance, pk=performance_id)
    performance.request_run = True
    performance.save()

    return redirect(reverse('project_performances', args=[application_id]))

@login_required
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
