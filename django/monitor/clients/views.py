import ipaddress
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import AlertsConfigSerializer, PrometheusConfigSerializer
from .models import AlertsConfig, PrometheusConfig

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
    return HttpResponse(status=200, content=ip.is_private)


def heartbeat(request):
    """
    Called by monitor_client to report status and detect lost of client.
    Require to be registered using register api.
    """
    return HttpResponse(status=200)