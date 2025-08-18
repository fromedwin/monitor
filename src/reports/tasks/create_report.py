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
    previous_report = ProjectReport.objects.filter(project=project).order_by('-created_at').first()

    # Create a simple report with status OK
    report_data = {
        "id": sha256(str(project.id).encode('utf-8')).hexdigest(),
        "project_id": project.id,
        "date": timezone.now().isoformat(),
        "pages": [
            {
                "url": project_url,
                "http_status": page.http_status,
                "title": page.title,
                "description": page.description,
                "lighthouse_report": page.lighthouse_report.first().report_json_file.url if page.lighthouse_report.first() else None,
                "lighthouse_report_date": page.lighthouse_report.first().creation_date if page.lighthouse_report.first() else None,
                "lighthouse_report_form_factor": page.lighthouse_report.first().form_factor if page.lighthouse_report.first() else None,
                "lighthouse_report_score_performance": page.lighthouse_report.first().score_performance if page.lighthouse_report.first() else None,
                "lighthouse_report_score_accessibility": page.lighthouse_report.first().score_accessibility if page.lighthouse_report.first() else None,
            }
            for page in project.pages.all()
        ],
        "previous_report": previous_report.data if previous_report else None,
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

