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

from .models import Performance
from .serializer import PerfromanceSerializer
from django.http import JsonResponse
from django.core import serializers

from workers.models import Server

LIGHTHOUSE_SCRAPE_INTERVAL_MINUTRES = 30

@api_view(["GET"])
def fetch_performance(request, server_id):
    """
    Return the next performance to scrape. Should be used by a worker as soon as it is ready to scrape a url.
    """
    get_object_or_404(Server, uuid=server_id)

    performance = Performance.objects.filter(Q(last_request_date__isnull=True) | Q(last_request_date__lt=timezone.now()-timedelta(minutes=LIGHTHOUSE_SCRAPE_INTERVAL_MINUTRES))).order_by('-creation_date')

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
def publish_report(request, server_id, performance_id):

    server = get_object_or_404(Server, uuid=id)

    # Get performance to update
    performance = get_object_or_404(Performance, id=performance_id)

    # Get JSON from POST
    data = json.loads(request.body.decode("utf-8"))

    return JsonResponse({})
