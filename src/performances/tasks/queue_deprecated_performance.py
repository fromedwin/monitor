# src/projects/tasks/refresh_favicon.py
from celery import shared_task, current_app
from django.utils import timezone
from datetime import timedelta
import logging
from performances.models import Performance
from itertools import chain

@shared_task(bind=True)
def queue_deprecated_performance(self):

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

    queue_name = 'fromedwin_lighthouse_queue'

    # Fetch performances that are older than 1 hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    performances = Performance.objects.filter(
        last_request_date__lt=one_hour_ago,
    )
    print(f'Found {performances.count()} performances to refresh after 1h.')

    for performance in performances:
        task_kwargs = {'id': performance.pk, 'url': performance.url}
        performance.last_request_date = timezone.now()
        performance.save()
        # Using pre-defined task_id to avoid revoking duplicate tasks
        current_app.send_task('fetch_lighthouse_report', kwargs=task_kwargs, queue=queue_name, task_id=f'performance_{performance.pk}')
