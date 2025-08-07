import logging
import json
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from projects.models import Project
from .models import ProjectReport
from logs.models import CeleryTaskLog


@api_view(["GET"])
def fetch_projects_needing_reports(request, secret_key):
    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)

    # Get projects that don't have any reports
    projects_without_reports = Project.objects.filter(
        project_report__isnull=True
    )

    logging.debug(f'Found {projects_without_reports.count()} projects to create reports for.')

    return JsonResponse({
        # List of ids and urls to fetch
        'projects': [{'id': project.pk, 'url': project.url} for project in projects_without_reports]
    })


@api_view(["POST"])
def save_report(request, secret_key, project_id):
    """
    Save a generated report for a specific project.
    """
    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized
        return JsonResponse({}, status=401)

    # Get project to update
    project = get_object_or_404(Project, id=project_id)

    # Load data from body as json
    data = json.loads(request.body.decode("utf-8"))
    report_data = data.get('report_data', {})
    duration = data.get('duration')

    # Create the report
    report = ProjectReport.objects.create(
        project=project,
        data=report_data
    )

    # Create a task log entry
    task_log = CeleryTaskLog.objects.create(
        project=project,
        task_name='report_task',
        duration=duration,
    )

    # Link the task log to the report
    report.celery_task_log = task_log
    report.save()

    logging.info(f'Saved report for project {project_id} with duration {duration}')

    return JsonResponse({
        'report_id': report.id,
        'status': 'success'
    })
