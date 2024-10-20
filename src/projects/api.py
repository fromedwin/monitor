from io import BytesIO
import json
import base64
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.template.defaultfilters import slugify

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import requests
from rest_framework.decorators import api_view

from .models import Project

from datetime import timedelta
from django.http import JsonResponse
from django.core import serializers

from workers.models import Server
from django.conf import settings

from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

@api_view(["GET"])
def fetch_deprecated_favicons(request, secret_key):
    """
    Return projects id and url which need a refresh of the token
    """

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
