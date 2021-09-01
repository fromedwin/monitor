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