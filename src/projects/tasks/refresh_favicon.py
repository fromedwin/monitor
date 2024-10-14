# src/projects/tasks/refresh_favicon.py
from celery import shared_task, current_app
from django.utils import timezone
from datetime import timedelta
from .fetch_favicon import fetch_favicon

@shared_task(bind=True)
def refresh_favicon(self):

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

    #
    # Fetch projects whih need to update favicons
    #
    from projects.models import Project

    six_hours_ago = timezone.now() - timedelta(hours=6)
    projects = Project.objects.filter(
        favicon_last_edited__lt=six_hours_ago,
    ).exclude(
        favicon_task_status='QUEUED'  # Exclude 'QUEUED' status
    )
    print(f'Found {projects.count()} projects to refresh favicon.')
    for project in projects:
        project.favicon_task_status = 'PENDING'
        project.save()
        fetch_favicon.delay(project.pk, project.url)
