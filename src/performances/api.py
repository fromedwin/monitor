from datetime import timedelta
import logging
import json
import base64
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view

from .models import Performance, Report
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

    # Filter per last request date OR request_run true or last request date undefined
    performances = Performance.objects.filter(Q(request_run=True) | Q(last_request_date__isnull=True) | Q(last_request_date__lt=deprecated_if_before))

    for performance in performances:
        performance.last_request_date = timezone.now()
        performance.save()

    return JsonResponse({
        # List of ids and urls to fetch
        'performances': [{'id': performance.pk, 'url': performance.url} for performance in performances]
    })


@api_view(["GET", "POST"])
def report_api(request, secret_key, performance_id):

    if request.method == "GET":
        # Use django settings secret_key to authenticate django worker
        if secret_key != settings.SECRET_KEY:
            # return http unauthorized if secret key doesn't match
            return JsonResponse({}, status=401)

        performance = get_object_or_404(Performance, id=performance_id)
        last_report = performance.reports.last()

        return JsonResponse({
            # List of ids and urls to fetch
            'id': performance.pk,
            'url': performance.url,
            'last_report_date': last_report.creation_date if last_report else None,
            'LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES': settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES
        })

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)
    
    # Get performance to update
    performance = get_object_or_404(Performance, id=performance_id)

    # Load data from body as json
    data = json.loads(request.body.decode("utf-8"))

    # Generate metadata used for file storage
    path = performance.directory_path()
    try:
        filename = f'{data["audits"]["final-screenshot"]["details"]["timestamp"]}'
    except:
        filename = f'{timezone.now().timestamp()}'

    # Generate report.json file
    json_file = json.dumps(data)
    json_file = json_file.encode('utf-8')
    report_json_file = default_storage.save(f'{path}/{filename}.json', ContentFile(json_file))

    # Generate screenshot.jpg from report json base64 value
    try:
        screenshot_as_a_string = data['audits']['final-screenshot']['details']['data']
        screenshot_as_a_string = screenshot_as_a_string.replace('data:image/jpeg;base64,', '')
        screenshot = default_storage.save(f'{path}/{filename}.jpg', ContentFile(base64.b64decode(screenshot_as_a_string)))
    except:
        screenshot = None

    # Look for form factor as `desktop` or `mobile`
    formFactor = LIGHTHOUSE_FORMFACTOR_CHOICES[0][0]
    if data['configSettings']['formFactor'] == 'mobile':
        formFactor = LIGHTHOUSE_FORMFACTOR_CHOICES[1][0]

    report = Report.objects.create(
        performance = performance,
        form_factor = formFactor,
        score_performance = data['categories']['performance']['score'],
        score_accessibility = data['categories']['accessibility']['score'],
        score_best_practices = data['categories']['best-practices']['score'],
        score_seo = data['categories']['seo']['score'],
        score_pwa = data['categories']['pwa']['score'],
        screenshot = screenshot,
        report_json_file = report_json_file,
    )
    report.save()

    # Set performance as not requested anymore
    performance.request_run = False
    performance.save()

    return JsonResponse({})
