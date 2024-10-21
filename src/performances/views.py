import requests
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.safestring import SafeString

from projects.models import Project
from .models import Performance, Report
from .forms import PerformanceForm
from core.decorators import waiting_list_approved_only

def get_domaines_from_performances(performances_list):
    domains = {}
    # For each performance object we extract the url and index by domain 
    for performance in performances_list:
        
        # If performance.url does not start with http:// or https:// we add it at the beginning
        if not performance.url.startswith('http://') and not performance.url.startswith('https://'):
            performance.url = 'https://' + performance.url

        # Extract domain from url
        domain = performance.url.split('/')[2]

        # if new domain, we create a default object
        if not domains.get(domain):
            domains[domain] = {
                'url': domain,
                'tree': []
            }

        """
            fund_page for each page will look for the proper depth to add it.
        """
        def find_page(pages, performance, depth=0, path_parent=''):
            # print('FIND_PAGE', pages, performance)
            path = '/'.join(performance.url.split('/')[3:])

            if path != '': #For root url we add directly
                for page in pages:
                    page_path = '/'.join(page['performance'].url.split('/')[3:])
                    # If root url is in pages, we go to children level directly
                    if page_path == '':
                        find_page(page['children'], performance, depth+1, page_path)
                        return
                    else:
                        if path.startswith(page_path):
                            if path != page_path:
                                find_page(page['children'], performance, depth+1, page_path)
                            return

            pages.append({
                'performance': performance,
                'path': path,
                'path_parent': path_parent,
                'path_without_parent': path.replace(path_parent, ''),
                'depth': depth,
                'report': None if not performance.reports.all else performance.reports.all().last(),
                'children': [],
            })

        # We start with the root page
        find_page(domains[domain]['tree'], performance)

    return domains

@login_required
@waiting_list_approved_only()
def project_performances(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    domains = get_domaines_from_performances(project.performances.all().order_by('url'))

    return render(request, 'project/performances.html', {
        'project': project,
        'performances_count': project.performances.count(),
        'domains': domains,
    })

@login_required
@waiting_list_approved_only()
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

        form = PerformanceForm(request.POST, instance=performance, project=project)

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
@waiting_list_approved_only()
def performance_delete(request, application_id, performance_id):
    """
        Delete service model
    """

    performance = get_object_or_404(Performance, pk=performance_id)
    performance.delete()

    return redirect(reverse('project_performances', args=[application_id]))

@login_required
@waiting_list_approved_only()
def performance_rerun(request, application_id, performance_id):
    """
        Delete service model
    """

    performance = get_object_or_404(Performance, pk=performance_id)
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

@login_required
@waiting_list_approved_only()
def performances_all(request):

    domains = {}
    for project in request.user.projects.all():
        # Merge domain dict with a new dict
        domains = {**domains, **get_domaines_from_performances(project.performances.all().order_by('url'))}

    return render(request, 'project/performances_all.html', {
        'user': request.user,
        'domains': domains
    })
