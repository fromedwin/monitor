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

@api_view(["GET"])
def next_performance(request):
    """
    Return the next performance to scrape. Should be used by a worker as soon as it is ready to scrape a url.
    """
    performance = Performance.objects.all().order_by('-creation_date')[0]

    return JsonResponse({
        # Perfromance object using serializer from django
        'performance': PerfromanceSerializer(performance).data
    })
