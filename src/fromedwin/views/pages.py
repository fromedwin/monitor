import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import Project
from fromedwin.decorators import waiting_list_approved_only

@login_required
@waiting_list_approved_only()
def project_pages(request, id):
    """
    Show current project status
    """

    project = get_object_or_404(Project, pk=id)

    # Filter out pages that are redirected to the same page but flagged because of tailslash redirect
    pages_redirected = project.pages.filter(http_status=301).order_by('url')
    pages_redirected_filtered = []
    for page in pages_redirected:
        url = page.url
        first_link = page.outbound_links.first()
        redirect_url = first_link.to_page.url if first_link else None
        if redirect_url and redirect_url != f'{url}/' or page.sitemap_last_seen is not None:
            pages_redirected_filtered.append(page)

    return render(request, 'pages/pages.html', {
        'project': project,
        'pages_count': project.pages.count(),
        'pages': project.pages.filter(http_status__lt=300).exclude(http_status=0).order_by('url'),
        'pages_redirected': pages_redirected_filtered,
        'pages_with_errors': project.pages.filter(
            Q(http_status__gte=400) | Q(http_status=0)
        ).order_by('url'),
        'pages_loading': project.pages.filter(http_status__isnull=True).order_by('url')
    })
