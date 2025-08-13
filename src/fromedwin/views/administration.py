from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.http import JsonResponse
from workers.models import Server
from availability.models import Service
from influxdb_client import InfluxDBClient
import logging

def get_stats_data():
    """
    Get administration statistics data
    """
    # InfluxDB connection settings
    url = settings.INFLUXDB_URL
    token = settings.INFLUXDB_TOKEN
    org = settings.INFLUXDB_ORG
    bucket = settings.INFLUXDB_BUCKET

    lighthouse_worker = 0
    celery_worker = 0
    fromedwin_queue = None
    lighthouse_queue = None

    # Connect to InfluxDB
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()

        start_time = (datetime.utcnow() - timedelta(minutes=1)).isoformat() + "Z"
        end_time = datetime.utcnow().isoformat() + "Z"
        # Define your Flux query
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: {start_time}, stop: {end_time})
            |> filter(fn: (r) => r["_measurement"] == "rabbitmq_prometheus")
            |> filter(fn: (r) => r["_field"] == "rabbitmq_queue_consumers")
            |> filter(fn: (r) => r["queue"] == "{settings.CELERY_QUEUE_LIGHTHOUSE}")
            |> aggregateWindow(every: 1m, fn: last, createEmpty: false)
            |> yield(name: "last")
        '''

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    lighthouse_worker = record.get_value()

        except Exception as e:
            lighthouse_worker = None
            logging.error(f'Error querying InfluxDB: {e}')

        
        # Define your Flux query
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: {start_time}, stop: {end_time})
            |> filter(fn: (r) => r["_measurement"] == "rabbitmq_prometheus")
            |> filter(fn: (r) => r["_field"] == "rabbitmq_queue_consumers")
            |> filter(fn: (r) => r["queue"] == "{settings.CELERY_QUEUE}")
            |> aggregateWindow(every: 1m, fn: last, createEmpty: false)
            |> yield(name: "last")
        '''

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    celery_worker = record.get_value()
        except Exception as e:
            celery_worker = None
            logging.error(f'Error querying InfluxDB: {e}')

        # Define your Flux query
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: {start_time}, stop: {end_time})
            |> filter(fn: (r) => r["_measurement"] == "rabbitmq_prometheus")
            |> filter(fn: (r) => r["_field"] == "rabbitmq_queue_messages")
            |> filter(fn: (r) => r["queue"] == "fromedwin_lighthouse_queue")
            |> last()
        '''

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    lighthouse_queue = record.get_value()
        except Exception as e:
            logging.error(f'Error querying InfluxDB: {e}')

        # Define your Flux query
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: {start_time}, stop: {end_time})
            |> filter(fn: (r) => r["_measurement"] == "rabbitmq_prometheus")
            |> filter(fn: (r) => r["_field"] == "rabbitmq_queue_messages")
            |> filter(fn: (r) => r["queue"] == "fromedwin_queue")
            |> last()
        '''

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    fromedwin_queue = record.get_value()
        except Exception as e:
            logging.error(f'Error querying InfluxDB: {e}')

    servers = Server.objects.filter(
        last_seen__gte=timezone.now() - timezone.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-creation_date')

    return {
        'users_count': User.objects.count(),
        'url_count': Service.objects.count(),
        'lighthouse_worker': lighthouse_worker,
        'celery_worker': celery_worker,
        'lighthouse_queue': lighthouse_queue,
        'fromedwin_queue': fromedwin_queue,
        'prometheus_workers': servers.count(),
        'settings': settings,
    }

@staff_member_required
def administration(request):
    """
    Show administration data
    """
    # Get stats data
    stats = get_stats_data()
    
    # if get success exist boolean true
    email_success = False
    email_fail = False
    
    if 'email_success' in request.GET:
        email_success = True
    
    if 'email_fail' in request.GET:
        email_fail = True

    servers = Server.objects.filter(
        last_seen__gte=timezone.now() - timezone.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-creation_date')

    return render(request, 'administration/administration.html', {
        'servers': servers,
        'settings': settings,
        'email_success': email_success,
        'email_fail': email_fail,
        'stats': stats
    })


@staff_member_required
def administration_stats_api(request):
    """
    Return administration statistics as JSON for AJAX calls
    """
    if request.method == 'GET':
        stats = get_stats_data()
        return JsonResponse(stats)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@staff_member_required
def test_email(request):

    success = True
    # Send test email
    try:
        send_mail(
            'Test email',
            'This is a test email',
            f"{settings.CONTACT_NAME} <{settings.CONTACT_EMAIL}>",
            [request.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)
        success = False

    return redirect(f"{reverse('administration')}{ '?email_success' if success else 'email_fail' }")
