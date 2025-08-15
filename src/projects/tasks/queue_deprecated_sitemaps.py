import logging
from celery import shared_task, current_app
from django.conf import settings
import requests
from .fetch_sitemap import fetch_sitemap
from django.utils import timezone
from datetime import timedelta
from projects.models import Project

@shared_task(bind=True)
def queue_deprecated_sitemaps(self):

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

    # Fetch projects which need to update sitemap
    one_day_ago = timezone.now() - timedelta(days=settings.TIMINGS['SITEMAP_INTERVAL_HOURS'])
    projects = Project.objects.filter(
        sitemap_last_edited__lt=one_day_ago,
    )

    logging.info(f'Found {len(list(projects))} projects to refresh sitemap.')

    for project in projects:
        logging.debug(f'Project {project.pk} has {project.sitemap_task_status} status and {project.sitemap_last_edited} value lower than {one_day_ago}.')
        project.sitemap_task_status = 'PENDING'
        project.save()  

    for project in projects:
        fetch_sitemap.delay(project.get('id'), project.get('url'))
