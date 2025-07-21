from datetime import timedelta
import json
import base64
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view

from projects.models import Pages
from logs.models import CeleryTaskLog
from .models import LighthouseReport
from django.http import JsonResponse

from django.conf import settings

from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

@api_view(["GET"])
def fetch_deprecated_performances(request, secret_key):
    """
    Return projects id and url which need a refresh of the token
    """

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)

    deprecated_if_before = timezone.now() - timedelta(minutes=settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES)
    print(f"Deprecated if before: {deprecated_if_before}")
    # Filter per last request date OR request_run true or last request date undefined
    pages = Pages.objects.filter(
        (Q(lighthouse_last_request__isnull=True) | Q(lighthouse_last_request__lt=deprecated_if_before)) & Q(http_status__lt=400)
    )
    print(f"Found {len(list(pages))} pages to refresh with the interval of {settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES} minutes.")
    for page in pages:
        page.lighthouse_last_request = timezone.now()
        page.save()

    return JsonResponse({
        # List of ids and urls to fetch
        'performances': [{'id': page.pk, 'url': page.url} for page in pages]
    })


@api_view(["GET", "POST"])
def report_api(request, secret_key, page_id):

    if request.method == "GET":
        # Use django settings secret_key to authenticate django worker
        if secret_key != settings.SECRET_KEY:
            # return http unauthorized if secret key doesn't match
            return JsonResponse({}, status=401)

        page = get_object_or_404(Pages, pk=page_id)
        last_report = page.lighthouse_report.first()

        return JsonResponse({
            # List of ids and urls to fetch
            'id': page.pk,
            'url': page.url,
            'last_report_date': last_report.creation_date if last_report else None,
            'LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES': settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES
        })

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)
    
    # Get performance to update
    page = get_object_or_404(Pages, pk=page_id)
    # Load data from body as json
    data = json.loads(request.body.decode("utf-8"))
    
    # Parse the report JSON string if it's a string (lighthouse returns JSON as string)
    if isinstance(data['report'], str):
        data['report'] = json.loads(data['report'])
        print("Parsed report from JSON string")

    # Generate metadata used for file storage
    path = page.project.directory_path()
    try:
        filename = f'{data["report"]["audits"]["final-screenshot"]["details"]["timestamp"]}'
    except:
        filename = f'{timezone.now().timestamp()}'

    # Generate report.json file
    json_file = json.dumps(data['report'])
    json_file = json_file.encode('utf-8')
    report_json_file = default_storage.save(f'{path}/{filename}.json', ContentFile(json_file))

    # Generate screenshot.jpg from report json base64 value
    try:
        screenshot_as_a_string = data['report']['audits']['final-screenshot']['details']['data']
        screenshot_as_a_string = screenshot_as_a_string.replace('data:image/jpeg;base64,', '')
        screenshot = default_storage.save(f'{path}/{filename}.jpg', ContentFile(base64.b64decode(screenshot_as_a_string)))
    except:
        screenshot = None

    # Look for form factor as `desktop` or `mobile`
    formFactor = LIGHTHOUSE_FORMFACTOR_CHOICES[0][0]
    if data['report']['configSettings']['formFactor'] == 'mobile':
        formFactor = LIGHTHOUSE_FORMFACTOR_CHOICES[1][0]

    celery_task_log = CeleryTaskLog.objects.create(
        project = page.project,
        task_name = 'lighthouse',
        duration = timedelta(milliseconds=data['duration']) if data['duration'] else None
    )

    report = LighthouseReport.objects.create(
        page = page,
        form_factor = formFactor,
        score_performance = data['report']['categories']['performance']['score'],
        score_accessibility = data['report']['categories']['accessibility']['score'],
        score_best_practices = data['report']['categories']['best-practices']['score'],
        score_seo = data['report']['categories']['seo']['score'],
        score_pwa = data['report']['categories']['pwa']['score'],
        screenshot = screenshot,
        report_json_file = report_json_file,
        celery_task_log = celery_task_log
    )
    report.save()

    return JsonResponse({})
