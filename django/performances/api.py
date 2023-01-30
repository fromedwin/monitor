import json
import datetime
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings

from rest_framework.decorators import api_view

from .models import Performance, Report
from .serializer import PerfromanceSerializer
from django.http import JsonResponse
from django.core import serializers

from workers.models import Server
from django.conf import settings

from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

@api_view(["GET"])
def fetch_performance(request, server_id):
    """
    Return the next performance to scrape. Should be used by a worker as soon as it is ready to scrape a url.
    """
    get_object_or_404(Server, uuid=server_id)

    performance = Performance.objects.filter(Q(last_request_date__isnull=True) | Q(last_request_date__lt=timezone.now()-timedelta(minutes=settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES))).order_by('-creation_date')

    # If no performance to work on, we return empty json 
    if performance:
        performance = performance[0]

        performance.last_request_date = timezone.now()
        performance.save()

        return JsonResponse({
            # Perfromance object using serializer from django
            'performance': PerfromanceSerializer(performance).data
        })
    else:
        return JsonResponse({})


@api_view(["POST"])
def save_report(request, server_id, performance_id):

    server = get_object_or_404(Server, uuid=server_id)

    # Get performance to update
    performance = get_object_or_404(Performance, id=performance_id)

    # Get JSON from POST
    data = json.loads(request.body.decode("utf-8"))
    # form factor specify if lighthouse report is for desktop or mobile
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
    )
    report.save()

    return JsonResponse({})
