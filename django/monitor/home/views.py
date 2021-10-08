from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from rest_framework.authtoken.models import Token
from django.shortcuts import render
from clients.models import Server
import datetime
from django.utils import timezone

from allauth.socialaccount.models import SocialApp

# Create your views here.
def index(request):

    token = None
    is_staff = False
    servers = []

    if not request.user.is_anonymous:
        is_staff = request.user.is_staff
        token = Token.objects.get(user=request.user)
        servers = Server.objects.filter(
            last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
        ).order_by('-last_seen')

    socialapps = SocialApp.objects.all()

    return render(request, 'index.html', {
        'servers': servers,
        'socialapps': socialapps,
        'token': token,
        'is_staff': is_staff,
        'settings': settings,
    })