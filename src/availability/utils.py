import logging
from django.conf import settings
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta

from .models import Service

def get_project_stats(project_id, duration=60*60):
    """"
        get_project_stats fetch project data from influxDB and bundle them into a dictionary
    """
    
    url = settings.INFLUXDB_URL
    token = settings.INFLUXDB_TOKEN
    org = settings.INFLUXDB_ORG
    bucket = settings.INFLUXDB_BUCKET

    stats = {}

    # Connect to InfluxDB
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()

        # Define your Flux query
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: -1d) 
            |> filter(fn: (r) => r["_field"] == "probe_http_status_code" or r["_field"] == "probe_http_ssl" or r["_field"] == "probe_http_redirects" or r["_field"] == "probe_http_version" or r["_field"] == "probe_tls_version_info" or r["_field"] == "probe_ssl_earliest_cert_expiry")
            |> filter(fn: (r) => r["project"] == "{project_id}")
            |> last()
        '''

        services = {}

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    service_name = record['service']
                    if service_name not in services:
                        services[service_name] = {
                            'title': Service.objects.get(pk=service_name).title,
                        }
                    services[service_name][record.get_field()] = record.get_value()

        except Exception as e:
            logging.error(f'Error querying InfluxDB: {e}')
        
        # Calculate time range
        time_range_stop = datetime.utcnow() - timedelta(seconds=60)
        time_range_start = time_range_stop - timedelta(seconds=duration)

        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: {time_range_start.isoformat()}Z, stop: {time_range_stop.isoformat()}Z)
            |> filter(fn: (r) => r["_measurement"] == "prometheus_remote_write")
            |> filter(fn: (r) => r["_field"] == "probe_duration_seconds")
            |> filter(fn: (r) => r["project"] == "{project_id}")
            |> aggregateWindow(every: 1m, fn: mean, createEmpty: true)
            |> fill(value: 0.0)
            |> yield(name: "mean")
        '''
        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    service_id = record['service']
                    if service_id not in services:
                        services[service_id] = {}
                    if 'duration_seconds' not in services[service_id]:
                        services[service_id]['duration_seconds'] = []
                    services[service_id]['duration_seconds'].append([record.get_time().strftime('%Y-%m-%dT%H:%M:%S'), record.get_value()])

        except Exception as e:
            logging.error(f'Error querying InfluxDB: {e}')

        stats['services'] = services

    return stats


def get_user_stats(user_id):
    """"
        get_project_stats fetch project data from influxDB and bundle them into a dictionary
    """
    
    url = settings.INFLUXDB_URL
    token = settings.INFLUXDB_TOKEN
    org = settings.INFLUXDB_ORG
    bucket = settings.INFLUXDB_BUCKET

    stats = {}

    # Connect to InfluxDB
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()

        # Define your Flux query
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: -1d) 
            |> filter(fn: (r) => r["_field"] == "probe_http_status_code" or r["_field"] == "probe_http_ssl" or r["_field"] == "probe_http_redirects" or r["_field"] == "probe_http_version" or r["_field"] == "probe_tls_version_info" or r["_field"] == "probe_ssl_earliest_cert_expiry")
            |> filter(fn: (r) => r["user"] == "{user_id}")
            |> last()
        '''

        services = {}

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    service_name = record['service']
                    if service_name not in services:
                        services[service_name] = {
                            'title': Service.objects.get(pk=service_name).title,
                        }
                    services[service_name][record.get_field()] = record.get_value()

        except Exception as e:
            logging.error(f'Error querying InfluxDB: {e}')
        
        stats['services'] = services

    return stats

def is_project_monitored(project_id):
    """
        Check if service is monitored
    """
    url = settings.INFLUXDB_URL
    token = settings.INFLUXDB_TOKEN
    org = settings.INFLUXDB_ORG
    bucket = settings.INFLUXDB_BUCKET

    result = False

    # Connect to InfluxDB
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()

        # Define your Flux query to return only the last value
        # Add a range to bound the query, e.g., last 1 day
        flux_query = f'''
        from(bucket: "{bucket}")
            |> range(start: -1d)
            |> filter(fn: (r) => r["_measurement"] == "prometheus_remote_write")
            |> filter(fn: (r) => r["_field"] == "probe_duration_seconds")
            |> filter(fn: (r) => r["project"] == "{project_id}")
            |> last()
        '''

        services = {}

        try:
            # Execute the query
            result = query_api.query(org=org, query=flux_query)
            for table in result:
                for record in table.records:
                    service_name = record['service']
                    if service_name not in services:
                        services[service_name] = {
                            'title': Service.objects.get(pk=service_name).title,
                        }
                    services[service_name][record.get_field()] = record.get_value()
                    if record.get_value() > 0:
                        result = True

        except Exception as e:
            logging.error(f'Error querying InfluxDB: {e}')
            raise e

    return result