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



from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from fromedwin.decorators import waiting_list_approved_only


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

    logging.info(f'Project {project_domain} has {len(urls)} pages in sitemap.')
    logging.info(f'{len(data.get('urls')) - len(list(urls))} urls got removed because they are not in the same domain.')

    if project.url not in urls:
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

    duration = data.get('duration')
    CeleryTaskLog.objects.create(
        project=project,
        task_name='sitemap_task',
        duration=timedelta(seconds=duration) if duration else None,
    )

    # Select all pages updates and trigger scraping
    pages = Pages.objects.filter(sitemap_last_seen=sitemap_last_edited, project=project)
    for page in pages:
        scrape_page.delay(page.pk, page.url)

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
@api_view(["DELETE"])
def delete_page(request, page_id):
    """
    Delete a page for authenticated users
    """
    try:
        page = get_object_or_404(Pages, pk=page_id)
        
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
