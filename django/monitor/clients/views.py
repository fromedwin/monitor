import ipaddress
import datetime
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import AlertsConfigSerializer, PrometheusConfigSerializer
from .models import AlertsConfig, PrometheusConfig, Server
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse

class AlertsConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AlertsConfig.objects.all()
    serializer_class = AlertsConfigSerializer

class PrometheusConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PrometheusConfig.objects.all()
    serializer_class = PrometheusConfigSerializer

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


def heartbeat(request, id):
    """
    Called by monitor_client to report status and detect lost of client.
    Require to be registered using register api.
    """
    server = get_object_or_404(Server, uuid=id)
    server.last_seen = datetime.datetime.now()
    server.save()

    return HttpResponse(status=200)