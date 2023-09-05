from django.shortcuts import render
from django.http import HttpResponse

from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from workers.models import Server

def restricted(request):
    return render(request, 'restricted.html')

#
# Set of views to monitor global application status
#
def healthcheck_database(request):

    # Send a request to database using django API to ensure database healthcheck is good
    
    # Catch error and return exception 
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")

        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)


def healthcheck_workers_availability(request):

    servers = Server.objects.filter(
        monitoring=True,
        last_seen__gte=timezone.now() - timezone.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-last_seen')

    # If there is more than 1 server we retur
    if len(servers) > 0:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


def healthcheck_workers_lighthouse(request):

    servers = Server.objects.filter(
        monitoring=True,
        last_seen__gte=timezone.now() - timezone.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-last_seen')

    # If there is more than 1 server we retur
    if len(servers) > 0:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)

