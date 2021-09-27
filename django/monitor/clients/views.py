import ipaddress
import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import AlertsConfigSerializer
from .models import AlertsConfig, Server
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.models import User


class AlertsConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AlertsConfig.objects.all()
    serializer_class = AlertsConfigSerializer

@api_view(['GET'])
def prometheus(request, id):
    """
    Fetched on start by monitor_client to introduce itself and get credentials
    """

    users = User.objects.filter(applications__isnull=False).distinct()

    yaml = render_to_string("prometheus_template.yml", { "users": users})

    # Should retur application/x-yaml
    return HttpResponse(yaml, content_type="text/plain")

@api_view(['GET'])
def register(request):
    """
    Fetched on start by monitor_client to introduce itself and get credentials
    """
    ip = ipaddress.IPv4Address(request.META['REMOTE_ADDR'])

    server = Server(ip=ip)
    server.save()

    return JsonResponse({
        'uuid': server.uuid
    })

@api_view(['GET'])
def heartbeat(request, id):
    """
    Called by monitor_client to report status and detect lost of client.
    Require to be registered using register api.
    """
    server = get_object_or_404(Server, uuid=id)
    server.last_seen = datetime.datetime.now()
    server.save()

    return HttpResponse(status=200)