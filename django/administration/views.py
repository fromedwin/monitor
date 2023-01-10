import datetime

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

from allauth.socialaccount.models import SocialApp
from rest_framework.authtoken.models import Token

from clients.models import Server

@staff_member_required
def administration(request):
    """
    Show administration data
    """
    token = None
    is_staff = False
    servers = []

    token = Token.objects.get(user=request.user)
    servers = Server.objects.filter(
        last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-last_seen')

    return render(request, 'administration.html', {
        'servers': servers,
        'token': token,
        'settings': settings,
    })

