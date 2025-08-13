import logging
import json
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from projects.models import Project
from projects.utils import get_project_task_status
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

    # Keep only those whose task status reports_status is PENDING
    projects_needing_reports = []
    for project in projects_without_reports:
        status = get_project_task_status(project)
        if status.get('reports_status') == 'PENDING':
            projects_needing_reports.append(project)

    logging.debug(f'Found {len(projects_needing_reports)} projects to create reports for (pending only).')

    # This code finds projects that already have at least one report,
    # but their most recent report was created more than 7 days ago.
    # It does this by:
    # 1. Calculating the datetime for 7 days ago.
    generate_reports_older_than = timezone.now() - timedelta(days=settings.TIMINGS['REPORT_INTERVAL_DAYS'])
    # 2. Filtering projects that have at least one related ProjectReport (project_report__isnull=False).
    # 3. Annotating each project with the latest 'creation_date' timestamp from its related reports.
    # 4. Filtering to only include projects whose latest report is older than 7 days.
    projects_with_old_reports = Project.objects.filter(
        project_report__isnull=False
    ).annotate(
        latest_report_time=models.Max('project_report__creation_date')
    ).filter(
        latest_report_time__lt=generate_reports_older_than
    )

    # Combine projects without reports and those with old reports, avoiding duplicates
    projects_needing_reports = list(projects_needing_reports) + [
        project for project in projects_with_old_reports
        if get_project_task_status(project).get('reports_status') == 'PENDING'
        and project not in projects_needing_reports
    ]


    return JsonResponse({
        # List of ids and urls to fetch
        'projects': [{'id': project.pk, 'url': project.url} for project in projects_needing_reports]
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
