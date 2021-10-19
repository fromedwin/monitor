from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from rest_framework.authtoken.models import Token
from django.shortcuts import render
from clients.models import Server
import datetime
from django.utils import timezone

from allauth.socialaccount.models import SocialApp

from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    if request.user.is_anonymous:

        socialapps = SocialApp.objects.all()
        return render(request, 'homepage.html', {
            'socialapps': socialapps,
        })

    token = None
    is_staff = False
    servers = []

    token = Token.objects.get(user=request.user)
    servers = Server.objects.filter(
        last_seen__gte=timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-last_seen')


    return render(request, 'dashboard.html', {
        'servers': servers,
        'token': token,
        'settings': settings,
    })

@login_required
def projects(request):

    return render(request, 'projects.html', {})