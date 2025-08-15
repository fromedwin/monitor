import logging
from celery import shared_task, current_app
from django.conf import settings
import requests
from .create_report import create_report
from projects.models import Project
from projects.utils.get_project_task_status import get_project_task_status
from django.utils import timezone
from datetime import timedelta
from django.db import models

@shared_task(bind=True)
def queue_report_creation(self):

    # Revoke all tasks with the same name currently queued
    inspector = current_app.control.inspect()
    active_tasks = inspector.active()
    reserved_tasks = inspector.reserved()

    task_name = self.name
    task_id = self.request.id

    # Helper function to revoke tasks
    def revoke_tasks(tasks):
        for worker, tasks_list in tasks.items():
            for task in tasks_list:
                if task['name'] == task_name and task['id'] != task_id:
                    current_app.control.revoke(task['id'], terminate=True)
                    print(f"Revoked task {task['id']} on worker {worker}")

    # Revoke tasks that are currently active
    if active_tasks:
        revoke_tasks(active_tasks)

    # Revoke tasks that are reserved (queued but not started)
    if reserved_tasks:
        revoke_tasks(reserved_tasks)


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

    print(projects_with_old_reports)
    # Simply merge projects without reports and those with old reports
    projects_needing_reports = list(projects_needing_reports) + list(projects_with_old_reports)


    print(projects_needing_reports)
    projects = [{'id': project.pk, 'url': project.url} for project in projects_needing_reports]

    logging.info(f'Found {len(list(projects))} projects needing reports.')

    for project in projects:
        create_report.delay(project.get('id'), project.get('url'))
        logging.info(f'Queuing report creation for project {project.get("id")} ({project.get("url")})')
