from datetime import timedelta
import time
from celery import shared_task
from django.shortcuts import get_object_or_404
from projects.models import Project
from reports.models import ProjectReport
from logs.models import CeleryTaskLog

@shared_task()
def create_report(project_id, project_url):
    """
    Create a report for a specific project.
    """
    start_time = time.time()

    # Get project to update
    project = get_object_or_404(Project, id=project_id)
    

    # Create a simple report with status OK
    report_data = {
        "pages": [
            {
                "url": project_url,
                "http_status": page.http_status,
            }
            for page in project.pages.all()
        ]
    }


    duration_seconds = time.time() - start_time,

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

