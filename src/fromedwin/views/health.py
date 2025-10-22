from django.http import HttpResponse

from django.utils import timezone
from django.conf import settings
from workers.models import Server
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def health_check(request):
    # Check database connectivity
    db_healthy = True
    try:
        for name in connections.databases:
            cursor = connections[name].cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
    except OperationalError:
        db_healthy = False

    # You can add more health checks here (cache, celery, etc.)
    status = 200 if db_healthy else 503
    health_status = {
        'status': 'healthy' if db_healthy else 'unhealthy',
        'database': 'up' if db_healthy else 'down',
    }

    return JsonResponse(data=health_status, status=status)

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

