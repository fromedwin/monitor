from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .tasks.scrape_page import scrape_page
from .models import Project, Pages
from django.views.decorators.http import require_GET
from fromedwin.decorators import waiting_list_approved_only
from .utils.get_project_task_status import get_project_task_status
from celery import current_app
from django.conf import settings

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

        source = 'refresh_page_data' # Specify this is a scheduled task so when workers fetch the report they can verify if still required based on scheduled interval
        task_kwargs = {'id': page.pk, 'url': page.url, 'source': source}
        current_app.send_task('fetch_lighthouse_report', kwargs=task_kwargs, queue=settings.CELERY_QUEUE_LIGHTHOUSE, task_id=f'performance_{page.pk}')
        
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
    data = get_project_task_status(project)
    return JsonResponse(data)
