import logging
import json
from datetime import timedelta
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
    Accepts JSON with keys: report_data (object), duration (seconds float or null)
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
    duration_seconds = data.get('duration')

    # Create the report
    report = ProjectReport.objects.create(
        project=project,
        data=report_data
    )

    # Normalize duration: convert float seconds to timedelta if provided
    duration_value = None
    if isinstance(duration_seconds, (int, float)):
        duration_value = timedelta(seconds=float(duration_seconds))

    # Create a task log entry
    task_log = CeleryTaskLog.objects.create(
        project=project,
        task_name='report_task',
        duration=duration_value,
    )

    # Link the task log to the report
    report.celery_task_log = task_log
    report.save()

    logging.info(f'Saved report for project {project_id} with duration {duration_value}')

    return JsonResponse({
        'report_id': report.id,
        'status': 'success'
    })


# Backward/alias endpoint compatible name
save_project_report = save_report
