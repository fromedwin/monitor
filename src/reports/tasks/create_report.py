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
    

    # Report should generate json contianing the following:
    # - status: OK, WARNING, or ERROR
    status = "OK"
    # - Incidents: availablility
    incidents = []
    # - https when expiring
    https_expiring = None
    # - Lighthouse performance average for all pages.
    #    - top 5 worst page to improve
    lighthouse_performance = {
        "average": 0,
        "top_5_worst": [],
    }
    #    - Trend compare to previous report +2% - 5% ...
    lighthouse_performance_trend = None
    # - Counters: pages, 404, 301
    counters = {
        "pages": 0,
        "404": 0,
        "301": 0,
    }


    # Create a simple report with status OK
    report_data = {
        "status": status,
        "incidents": [],
        "https_expiring": None,
        "lighthouse_performance": {
            "average": 0,
            "top_5_worst": [],
        },
        "lighthouse_performance_trend": None,   
        "counters": {
            "pages": 0,
            "404": 0,
            "301": 0,
        },
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
