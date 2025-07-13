from django.conf import settings
from celery import current_app
from django.utils import timezone

def request_lighthouse_report(page, source):
    """
    Request a lighthouse report for a page
    """
    page.lighthouse_last_request = timezone.now()
    page.save()
    current_app.send_task(
        'fetch_lighthouse_report', 
        kwargs={
            'id': page.pk, 
            'url': page.url,
            'source': source,
        }, 
        queue=settings.CELERY_QUEUE_LIGHTHOUSE, 
        task_id=f'performance_{page.pk}')