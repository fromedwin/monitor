import ipaddress
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Metrics, Server, AuthBasic
from incidents.models import INCIDENT_SEVERITY_CHOICES

@api_view(['GET'])
def alerts(request, id):
    """
    Fetched on start by monitor_client to introduce itself and get credentials
    """
    get_object_or_404(Server, uuid=id)

    users = User.objects.filter(Q(projects__isnull=False)).distinct()

    yaml = render_to_string("alerts_template.yml", {
        "severity": INCIDENT_SEVERITY_CHOICES,
        "settings": settings,
    })

    # Should retur application/x-yaml
    return HttpResponse(yaml, content_type="text/plain")

@api_view(['GET'])
def prometheus(request, id):
    """
    Fetched on start by monitor_client to introduce itself and get credentials
    """
    server = get_object_or_404(Server, uuid=id)

    users = User.objects.filter(Q(projects__isnull=False)).distinct()

    metrics = Metrics.objects.all()

    yaml = render_to_string("prometheus_template.yml", {
        "server": server,
        "users": users,
        "metrics": metrics,
        "settings": settings,
    })

    # Should retur application/x-yaml
    return HttpResponse(yaml, content_type="text/plain")


@api_view(['GET'])
def alertmanager(request, id):
    """
    Fetched on start by monitor_client to introduce itself and get credentials
    """
    get_object_or_404(Server, uuid=id)

    yaml = render_to_string('alertmanager_template.yml', {
        "settings": settings,
    })

    # Should retur application/x-yaml
    return HttpResponse(yaml, content_type="text/plain")

@api_view(['GET'])
def register(request, secret_key):
    """
    Fetched on start by monitor_client to introduce itself and get credentials
    """

    # Use django settings secret_key to authenticate django worker
    if secret_key != settings.SECRET_KEY:
        # return http unauthorized if secret key doesn't match
        return JsonResponse({}, status=401)

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

    # Default value is 1 as default worker enable lighthouse and prometheus
    server.performance = request.GET.get('performance', '1') == '1'
    server.monitoring = request.GET.get('monitoring', '1') == '1'

    # Update last seen
    server.last_seen = timezone.now()
    server.save()

    return JsonResponse({
        'last_modified_setup': server.last_modified_setup
    })
