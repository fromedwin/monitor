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

from performances.models import Performance
from .models import Project

@api_view(["GET"])
def fetch_deprecated_favicons(request, secret_key):
    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)

    six_hours_ago = timezone.now() - timedelta(hours=6)
    projects = Project.objects.filter(
        favicon_last_edited__lt=six_hours_ago,
    )

    for project in projects:
        project.favicon_task_status = 'PENDING'
        project.save()

    return JsonResponse({
        # List of ids and urls to fetch
        'projects': [{'id': project.pk, 'url': project.url} for project in projects]
    })

@api_view(["GET"])
def fetch_deprecated_sitemaps(request, secret_key):
    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)

    one_day_ago = timezone.now() - timedelta(hours=24)
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
def save_favicon(request, secret_key, project_id):

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized
        return JsonResponse({}, status=401)

    # Get performance to update
    project = get_object_or_404(Project, id=project_id)

    # Load data from body as json
    data = json.loads(request.body.decode("utf-8"))
    favicon_url = data.get('favicon_url')

    # If favicon_url is null or undefined, it means worker couldn't find a favicon
    # We then set the status to FAILURE so we can react and retry if needed
    if not favicon_url:
        project.favicon_task_status = 'FAILURE'
        project.favicon_last_edited = timezone.now()
        project.save()
        return JsonResponse({})
    
    # Generate data for the favicon
    favicon_content_base64 = data.get('favicon_content')
    favicon_content = base64.b64decode(favicon_content_base64)
    favicon_content = BytesIO(favicon_content)

    project.favicon.save(data.get('favicon_url').split('/')[-1], favicon_content)
    project.favicon_task_status = 'SUCCESS'
    project.favicon_last_edited = timezone.now()
    project.save()

    return JsonResponse({})

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

    # Update sitemap_last_edited to pause fetching until deprecated
    project.sitemap_last_edited = timezone.now()
    project.save()

    if len(list(urls)) < 300:
        logging.info(f'Project {project.url} has less than 300 pages in sitemap.')
        Performance.objects.bulk_create(
            [
                Performance(project=project, url=url) for url in urls
            ],
            ignore_conflicts=True  # This avoids inserting rows that violate uniqueness constraints
        )
    else:
        logging.warning(f'Project {project.url} has more than 300 pages in sitemap, ignored for now.')

    return JsonResponse({})
