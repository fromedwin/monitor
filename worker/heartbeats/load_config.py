import os
import requests
import json
from dotenv import load_dotenv
import datetime
import time

headers = {
    'User-Agent': 'FromEdwinBot Python load_config',
}

def retry_request(url, max_retries=3, base_delay=1, method='GET'):
    """Retry a request with exponential backoff"""
    for attempt in range(max_retries):
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as err:
            if attempt == max_retries - 1:
                raise err
            delay = base_delay * (2 ** attempt)
            print(f'Request failed (attempt {attempt + 1}/{max_retries}): {err}. Retrying in {delay}s...')
            time.sleep(delay)

# Fetch Prometheur, alertmanager, and alert rules from server_url
def load_config(url=None, uuid=None):

    load_dotenv()

    DISABLE_MONITORING = os.environ.get("DISABLE_MONITORING", '0')

    if DISABLE_MONITORING == '1' or DISABLE_MONITORING == 1:
        print('❌ DISABLE_MONITORING == 1, disabling prometheus monitoring')
        return

    # Server url
    SERVER_URL = os.environ.get("SERVER_URL") or url

    # Fetch PROMETHEUS configuration files
    SERVER_PROMETHEUS_CONFIG_URL = f'{SERVER_URL}/clients/prometheus/{uuid}/'
    print(f'Loading PROMETHEUS configuration files at {SERVER_PROMETHEUS_CONFIG_URL}')
    try:
        response = retry_request(SERVER_PROMETHEUS_CONFIG_URL, method='GET')
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
    else:
        content = response.text
        print(f'> Prometheus have been loaded from {SERVER_URL}')
        with open(f'{os.path.dirname( __file__ )}/../prometheus/prometheus.yml', 'w') as file:
            file.write(content)
            file.close()

    # Fetch ALERTS configuration files
    SERVER_ALERTS_CONFIG_URL = f'{SERVER_URL}/clients/alerts/{uuid}/'
    print(f'Loading ALERTS configuration files at {SERVER_ALERTS_CONFIG_URL}')
    try:
        response = retry_request(SERVER_ALERTS_CONFIG_URL, method='GET')
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
    else:
        content = response.text
        print(f'> Alerts have been loaded from {SERVER_URL}')
        with open(f'{os.path.dirname( __file__ )}/../prometheus/alerts/alerts.yml', 'w') as file:
            file.write(content)
            file.close()


    # Fetch ALERTMANAGER configuration files
    SERVER_ALERTMANAGER_CONFIG_URL = f'{SERVER_URL}/clients/alertmanager/{uuid}/'
    print(f'Loading ALERTMANAGER configuration files at {SERVER_ALERTMANAGER_CONFIG_URL}')
    try:
        response = retry_request(SERVER_ALERTMANAGER_CONFIG_URL, method='GET')
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
    else:
        content = response.text
        print(f'> Alertmanager have been loaded from {SERVER_URL}')
        with open(f'{os.path.dirname( __file__ )}/../alertmanager/alertmanager.yml', 'w') as file:
            file.write(content)
            file.close()

    # When all config files are locally stored, 
    # script notify prometheus and alertmanager to reload.
    try:
        print('Reloading Prometheus configuration...')
        retry_request('http://prometheus:9090/-/reload')
        print('✅ Prometheus configuration reloaded successfully')
    except Exception as err:
        print(f'❌ Prometheus reload failed after retries: {err}')

    try:
        print('Reloading Alertmanager configuration...')
        retry_request('http://alertmanager:9093/-/reload')
        print('✅ Alertmanager configuration reloaded successfully')
    except Exception as err:
        print(f'❌ Alertmanager reload failed after retries: {err}')
