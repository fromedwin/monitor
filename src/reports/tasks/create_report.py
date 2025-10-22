from datetime import timedelta
import time
from celery import shared_task
from django.utils import timezone
from django.shortcuts import get_object_or_404
from projects.models import Project
from reports.models import ProjectReport
from logs.models import CeleryTaskLog
from hashlib import sha256
from availability.utils import get_project_stats

@shared_task()
def create_report(project_id, source='unknown'):
    """
    Create a report for a specific project.
    """
    start_time = time.time()

    # Get project to update
    project = get_object_or_404(Project, id=project_id)
    
    # Get the previous report for this project, if any
    previous_report = ProjectReport.objects.filter(project=project).order_by('-creation_date').first()
    if source == 'scheduler' and previous_report and previous_report.creation_date > timezone.now() - timedelta(minutes=5):
        print(f'Report for project {project.pk} is less than 5 minutes old, skipping...')
        return

    stats = get_project_stats(project_id, 60)
    # Remove duration_seconds values equal to 0 for each service
    for service in stats.get('services', {}).values():
        if 'duration_seconds' in service:
            # Instead of an array, set to the first non-null value (or None if none found)
            non_null_entries = [entry for entry in service['duration_seconds'] if entry[1] is not None]
            service['duration_timestamp'] = non_null_entries[0][0] if non_null_entries else None
            service['duration_seconds'] = non_null_entries[0][1] if non_null_entries else None

    previous_report_data = (
        {
            key: value
            for key, value in previous_report.data.items()
            if key != "previous_report"
        } if previous_report else None
    )

    # Create a simple report with status OK
    report_data = {
        "id": sha256(str(project.id).encode('utf-8')).hexdigest(),
        "project_id": project.id,
        "date": timezone.now().isoformat(),
        "performance_score": project.performance_score() or None,
        'services': stats['services'],
        "availability": {
            "7": project.availability(days=7),
            "30": project.availability(days=30),
            "incidents_count": project.incidents_count(),
        },
        "pages": [
            {
                "url": page.url,
                "http_status": page.http_status,
                "title": page.title or None,
                "description": page.description or None,
                "redirected_url": page.outbound_links.first().to_page.url if page.http_status == 301 and page.outbound_links.exists() else None,
                "lighthouse_report": (
                    {
                        "id": lh.id,
                        "score_performance": lh.score_performance,
                        "score_accessibility": lh.score_accessibility,
                        "score_best_practices": lh.score_best_practices,
                        "score_seo": lh.score_seo,
                        "score_pwa": lh.score_pwa,
                    } if (lh := page.lighthouse_report.first()) else None
                ),
            }
            for page in project.pages.all()
        ],
        "previous_report": previous_report_data,
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

