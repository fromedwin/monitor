import logging
import requests
import time
from celery import shared_task
from django.conf import settings


@shared_task()
def create_report(project_id, project_url):
    """
    Create a report for a specific project.
    """
    start_time = time.time()
    
    # Create a simple report with status OK
    report_data = {
        "status": "OK"
    }
    
    try:
        response = requests.post(f'{settings.BACKEND_URL}/api/save_project_report/{settings.SECRET_KEY}/{project_id}/', json={
            'report_data': report_data,
            'duration': time.time() - start_time,
        })
        response.raise_for_status()
        logging.info(f'Created report for project {project_id} ({project_url})')
    except Exception as e:
        logging.error(f"Error sending the result to the backend: {e}")
