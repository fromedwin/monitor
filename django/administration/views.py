import datetime

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required

from allauth.socialaccount.models import SocialApp

from workers.models import Server

from django.db.models import Q
from performances.models import Performance
from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

@staff_member_required
def administration(request):
    """
    Show administration data
    """
    token = None
    is_staff = False
    servers = []

    servers = Server.objects.filter(
        monitoring=True,
        last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-last_seen')

    inQueueLighthouse = Performance.objects.filter(Q(request_run=True) | Q(last_request_date__isnull=True) | Q(last_request_date__lt=timezone.now()-timedelta(minutes=settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES))).count()

    return render(request, 'administration.html', {
        'servers': servers,
        'settings': settings,
        'stats': {
            'inQueueLighthouse': inQueueLighthouse,
        }
    })
