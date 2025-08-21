from datetime import timedelta
import time
from celery import shared_task
from django.utils import timezone
from django.shortcuts import get_object_or_404
from projects.models import Project
from reports.models import ProjectReport
from logs.models import CeleryTaskLog
from hashlib import sha256

@shared_task()
def create_report(project_id, project_url):
    """
    Create a report for a specific project.
    """
    start_time = time.time()

    # Get project to update
    project = get_object_or_404(Project, id=project_id)
    
    # Get the previous report for this project, if any
    previous_report = ProjectReport.objects.filter(project=project).order_by('-creation_date').first()

    # Create a simple report with status OK
    report_data = {
        "id": sha256(str(project.id).encode('utf-8')).hexdigest(),
        "project_id": project.id,
        "date": timezone.now().isoformat(),
        "pages": [
            {
                "url": page.url,
                "http_status": page.http_status,
                "title": page.title or None,
                "description": page.description or None,
                "redirected_url": page.outbound_links.first().to_page.url if page.http_status == 301 else None,
            }
            for page in project.pages.all()
        ],
        "previous_report": previous_report.data if previous_report else None,
    }

    # Create the report
    report = ProjectReport.objects.create(
        project=project,
        data=report_data
    )

    # Normalize duration: convert float seconds to timedelta if provided
    duration = time.time() - start_time

    # Create a task log entry
    task_log = CeleryTaskLog.objects.create(
        project=project,
        task_name='report_task',
        duration=timedelta(seconds=duration) if duration else None,
    )

    # Link the task log to the report
    report.celery_task_log = task_log
    report.save()

