from io import BytesIO
import json
import base64
import logging
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from .tasks.scrape_page import scrape_page
from .models import Project, Pages, PageLink
from logs.models import CeleryTaskLog
from django.db import transaction
from django.views.decorators.http import require_GET
from fromedwin.decorators import waiting_list_approved_only
from availability.utils import is_project_monitored
from workers.models import Server

@api_view(["GET"])
def fetch_deprecated_sitemaps(request, secret_key):
    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)

    one_day_ago = timezone.now() - timedelta(days=1)
    projects = Project.objects.filter(
        sitemap_last_edited__lt=one_day_ago,
    )

    for project in projects:
        logging.debug(f'Project {project.pk} has {project.sitemap_task_status} status and {project.sitemap_last_edited} value lower than {one_day_ago}.')
        project.sitemap_task_status = 'PENDING'
        project.save()

    return JsonResponse({
        # List of ids and urls to fetch
        'projects': [{'id': project.pk, 'url': project.url} for project in projects]
    })



@api_view(["POST"])
def save_sitemap(request, secret_key, project_id):

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized
        return JsonResponse({}, status=401)

    # Get performance to update
    project = get_object_or_404(Project, id=project_id)

    # Load data from body as json
    data = json.loads(request.body.decode("utf-8"))
    urls = data.get('urls')

    sitemap_last_edited = timezone.now()

    # Only keep urls which have the same domain as the project url
    project_domain = project.url.split('/')[2]
    urls = [url for url in urls if project_domain in url]

    # Update sitemap_last_edited to pause fetching until deprecated
    project.sitemap_last_edited = sitemap_last_edited
    project.save()

    # If no urls from sitemap, we create a page for the project url
    if len(urls) == 0:
        page, created = Pages.objects.get_or_create(project=project, url=project.url)
        scrape_page.delay(page.pk, page.url)
    else:
        # Add project URL in list of pages to scrape but ignore same url if sitemap contains tailslash
        isProjectUrlSlashTailed = project.url.endswith('/')
        if isProjectUrlSlashTailed and project.url[:-1] not in urls and project.url not in urls:
            urls.append(project.url) # Add project url to the list of pages

        if not isProjectUrlSlashTailed and f'{project.url}/' not in urls and project.url not in urls:
            urls.append(project.url) # Add project url to the list of pages
        
        # Create new pages
        Pages.objects.bulk_create(
            [
                Pages(project=project, url=url, sitemap_last_seen=sitemap_last_edited) for url in urls
            ],
            ignore_conflicts=True  # This avoids inserting rows that violate uniqueness constraints
        )
        # Update existing pages data
        Pages.objects.filter(project=project, url__in=urls).update(sitemap_last_seen=sitemap_last_edited)

        # Send scraping request for all pages
        pages = Pages.objects.filter(sitemap_last_seen=sitemap_last_edited, project=project)
        for page in pages:
            scrape_page.delay(page.pk, page.url)

    # Save log about sitemap task
    duration = data.get('duration')
    CeleryTaskLog.objects.create(
        project=project,
        task_name='sitemap_task',
        duration=timedelta(seconds=duration) if duration else None,
    )

    return JsonResponse({})


@api_view(["POST"])
def save_scaping(request, secret_key, page_id):

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized
        return JsonResponse({}, status=401)

    # Get performance to update
    page = get_object_or_404(Pages, id=page_id)

    # Load data from body as json
    data = json.loads(request.body.decode("utf-8"))
    urls = []
    
    page.http_status = data.get('http_status', 0)
    if data.get('redirected_url') and data.get('http_status') == 301:
        page.save()
        to_page, created = Pages.objects.get_or_create(
            url=data.get('redirected_url'),
            project=page.project,
        )
        PageLink.objects.filter(from_page=page).delete()
        # Create the link (no need for get_or_create since we deleted all links above)
        PageLink.objects.create(
            from_page=page,
            to_page=to_page
        )

    elif data.get('http_status') == 404:
        page.save()
        PageLink.objects.filter(from_page=page).delete()
    else:
        page.title = data.get('title', '')
        page.description = data.get('description', '')
        page.scraping_last_seen = timezone.now()
        page.save()

        # get urls and create pages for each url. Might already exist then should ignore
        urls = data.get('urls', [])
        
        # Use transaction to ensure atomicity and prevent database locks
        with transaction.atomic():
            # Delete all existing outbound links from this page first (clean slate)
            PageLink.objects.filter(from_page=page).delete()
            
            # Create new links for all discovered URLs
            for url in urls:
                # Prevent a page from linking to itself
                # Ignore if the URL is the same as the current page, or if it doesn't start with the full domain (scheme + netloc)
                from urllib.parse import urlparse
                page_parsed = urlparse(page.url)
                url_parsed = urlparse(url)
                page_base = f"{page_parsed.scheme}://{page_parsed.netloc}"
                url_base = f"{url_parsed.scheme}://{url_parsed.netloc}"
                if url == page.url or url_base != page_base:
                    continue
                # Get or create the target page within the same project
                to_page, created = Pages.objects.get_or_create(
                    url=url,
                    project=page.project,
                )

                # Create the link (no need for get_or_create since we deleted all links above)
                PageLink.objects.create(
                    from_page=page,
                    to_page=to_page
                )
    
    # Save log about sitemap task
    duration = data.get('duration')
    log = CeleryTaskLog.objects.create(
        project=page.project,
        task_name='scraping_task',
        duration=timedelta(seconds=duration) if duration else None,
    )

    page.scraping_task_log = log
    page.save()

    return JsonResponse({
        'total_urls': len(urls)
    })

@require_GET
def project_pages_tree_json(request, project_id):
    """
    Returns a JSON tree of all pages in a project, organized by URL path,
    ignoring domain and http(s) parts.
    """
    from urllib.parse import urlparse

    project = get_object_or_404(Project, pk=project_id)
    pages = Pages.objects.filter(project=project).values('id', 'url', 'title')

    # Build a tree from URLs
    tree = {"name": project.title, "url": project.url, "children": []}

    for page in pages:
        url = page['url']
        # Parse the URL and get only the path, ignoring scheme and domain
        parsed = urlparse(url)
        path = parsed.path
        # Remove empty parts (from leading/trailing slashes)
        parts = [p for p in path.split('/') if p]
        current = tree
        for i, part in enumerate(parts):
            if 'children' not in current:
                current['children'] = []
            # Find if this part already exists
            found = None
            for child in current['children']:
                if child.get('name') == part:
                    found = child
                    break
            if not found:
                # If this is the last part, attach page info
                if i == len(parts) - 1:
                    node = {
                        "name": part,
                        "url": url,
                        "title": page.get('title') or part,
                        "page_id": page['id'],
                        "children": [],
                        "collapsed": False
                    }
                else:
                    node = {
                        "name": part,
                        "children": []
                    }
                current['children'].append(node)
                found = node
            current = found

    return JsonResponse(tree, safe=False)


@waiting_list_approved_only()
@api_view(["POST"])
def refresh_page_data(request, page_id):
    """
    Trigger a refresh/scrape for a specific page for authenticated users
    """
    try:
        page = get_object_or_404(Pages, pk=page_id)
        
        # Check if user has access to the project that owns this page
        if page.project.user != request.user:
            return JsonResponse({'error': 'Unauthorized access to this page'}, status=403)
        
        # Update the lighthouse_last_request timestamp to mark it as queued
        # from django.utils import timezone
        # page.lighthouse_last_request = timezone.now()
        # page.save()
        
        # Trigger the scraping task
        scrape_page.delay(page.pk, page.url)
        
        return JsonResponse({
            'success': True,
            'message': f'Refresh request sent for "{page.title or page.url}". Data will be updated shortly.'
        })
            
    except Pages.DoesNotExist:
        return JsonResponse({'error': 'Page not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error refreshing page: {str(e)}'}, status=500)


@waiting_list_approved_only()
@api_view(["DELETE"])
def delete_page(request, page_id):
    """
    Delete a page for authenticated users
    """
    try:
        page = get_object_or_404(Pages, id=page_id)
        
        # Check if user has access to the project that owns this page
        if page.project.user != request.user:
            return JsonResponse({'error': 'Unauthorized access to this page'}, status=403)
        
        # Store page info for response
        page_url = page.url
        page_title = page.title
        
        # Delete the page
        page.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Page "{page_title or page_url}" has been deleted successfully'
        })
            
    except Pages.DoesNotExist:
        return JsonResponse({'error': 'Page not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error deleting page: {str(e)}'}, status=500)

@waiting_list_approved_only()
@api_view(["GET"])
def project_task_status(request, project_id):
    """Get the status of all tasks for a project"""
    project = get_object_or_404(Project, id=project_id)
    pages = Pages.objects.filter(project=project)

    #
    # FAVICON Check if there's a recent favicon task log
    #
    recent_favicon_log = CeleryTaskLog.objects.filter(
        project=project,
        task_name='favicon_task'
    ).order_by('-created_at').first()
    favicon_status = 'SUCCESS' if recent_favicon_log else 'UNKNOWN'
    
    #
    # SITEMAP Get sitemap status
    #
    sitemap_status = project.sitemap_task_status
    
    # Check if there's a recent sitemap task log
    recent_sitemap_log = CeleryTaskLog.objects.filter(
        project=project,
        task_name='sitemap_task'
    ).order_by('-created_at').first()
    sitemap_status = 'SUCCESS' if recent_sitemap_log else 'UNKNOWN'

    #
    # SCRAPING
    # Get scraping status for all pages
    #
    scraping_status = 'UNKNOWN'
    scraping_progress = None
    
    if pages.exists():
        # Check if any page is still being scraped
        pages_without_scraping = pages.filter(scraping_last_seen__isnull=True)
        pages_with_status = pages.filter(http_status__isnull=False)
        total_pages = pages.count()
        completed_pages = pages_with_status.count()
        
        if pages_without_scraping.exists():
            scraping_status = 'PENDING'
            scraping_progress = {
                'total': total_pages,
                'completed': completed_pages
            }
            if total_pages == completed_pages:
                scraping_status = 'SUCCESS'
        else:
            # Check if any page has failed scraping (no http_status)
            pages_without_status = pages.filter(http_status__isnull=True)
            if pages_without_status.exists():
                scraping_status = 'PENDING'
            else:
                scraping_status = 'SUCCESS'
                scraping_progress = {
                    'total': total_pages,
                    'completed': completed_pages
                }
    
    # 
    # LIGHTHOUSE
    # Get lighthouse status
    #
    lighthouse_status = 'UNKNOWN'
    lighthouse_progress = None
    
    if pages.exists():
        from lighthouse.models import LighthouseReport
        
        # Only run lighthouse on 200x http code pages
        pages_http_200 = pages.filter(http_status__lt=300)
        pages_without_lighthouse = pages_http_200.filter(lighthouse_last_request__isnull=True)
        pages_with_reports = []
        pages_done = []
        for page in pages_http_200:
            if LighthouseReport.objects.filter(page=page).exists():
                pages_with_reports.append(page)
            elif page.http_status and page.http_status >= 300:
                # Pages with 300+ status codes are considered done (no lighthouse needed)
                pages_done.append(page)
        
        total_pages = pages_http_200.count()
        completed_pages = len(pages_with_reports) + len(pages_done)
        
        if pages_without_lighthouse.exists():
            lighthouse_status = 'PENDING'
            lighthouse_progress = {
                'total': total_pages,
                'completed': completed_pages
            }
            if total_pages == completed_pages:
                lighthouse_status = 'SUCCESS'
        else:
            # Check if any page has failed lighthouse (no lighthouse reports and not 300+ status)
            pages_without_reports = []
            for page in pages:
                if not LighthouseReport.objects.filter(page=page).exists() and (not page.http_status or page.http_status < 300):
                    pages_without_reports.append(page)
            if pages_without_reports:
                lighthouse_status = 'PENDING'
                lighthouse_progress = {
                    'total': total_pages,
                    'completed': completed_pages
                }
            else:
                lighthouse_status = 'SUCCESS'
                lighthouse_progress = {
                    'total': total_pages,
                    'completed': completed_pages
                }

    #
    # PROMETHEUS
    #
    # Get the project's creation date
    project_date = project.created_at
    # get server last_modified_setup
    server = Server.objects.last()
    last_seen = server.last_seen if server else None
    # Initialize prometheus status
    prometheus_status = 'UNKNOWN'
    
    if project_date and last_seen:
        # Check if project was created before the last server config update
        project_before_last_report = project_date < last_seen
        
        if project_before_last_report:
            # Project was created before last config update, check if it's being monitored
            prometheus_status = 'SUCCESS' if is_project_monitored(project_id) else 'PENDING'
        else:
            # Project was created after last config update, wait for server to pick up new config
            prometheus_status = 'DEPLOYING'
    else:
        # No server or project date info, fall back to monitoring check
        prometheus_status = 'SUCCESS' if is_project_monitored(project_id) else 'PENDING'

    #
    # REPORTS
    # Check if reports are available for the project
    #
    reports_status = 'WAITING'
    reports_progress = None

    if (
        favicon_status == 'SUCCESS' and
        sitemap_status == 'SUCCESS' and
        scraping_status == 'SUCCESS' and
        lighthouse_status == 'SUCCESS' and
        prometheus_status == 'SUCCESS'
    ):
        reports_status = 'PENDING'
    #
    #  ALL_COMPLETE
    #
    all_complete = (
        favicon_status == 'SUCCESS' and
        sitemap_status == 'SUCCESS' and
        scraping_status == 'SUCCESS' and
        lighthouse_status == 'SUCCESS' and
        prometheus_status == 'SUCCESS' and
        reports_status == 'SUCCESS'
    )
    
    return JsonResponse({
        'favicon_status': favicon_status,
        'sitemap_status': sitemap_status,
        'prometheus_status': prometheus_status,
        'scraping_status': scraping_status,
        'scraping_progress': scraping_progress,
        'lighthouse_status': lighthouse_status,
        'lighthouse_progress': lighthouse_progress,
        'reports_status': reports_status,
        'reports_progress': reports_progress,
        'all_complete': all_complete,
        'project_id': project_id
    })
