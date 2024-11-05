import logging
import requests
from celery import shared_task, current_app
from django.conf import settings

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

    #
    # Fetch backend to queue deprecated favicons
    #
    response = requests.get(f'{settings.BACKEND_URL}/api/fetch_deprecated_performances/{settings.SECRET_KEY}/')
    response.raise_for_status()
    performances = response.json().get('performances', [])

    logging.info(f'Found {len(list(performances))} performances to refresh with the interval of {settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES} minutes.')

    source = 'scheduler' # Specify this is a scheduled task so when workers fetch the report they can verify if still required based on scheduled interval
    for performance in performances:
        task_kwargs = {'id': performance.get('id'), 'url': performance.get('url'), 'source': source}
        current_app.send_task('fetch_lighthouse_report', kwargs=task_kwargs, queue=settings.CELERY_QUEUE_LIGHTHOUSE, task_id=f'performance_{performance.get('id')}')
