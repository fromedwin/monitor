import requests
from django.template.loader import render_to_string

def generate_alert_manager_config():
    """

    """
    from notifications.models import Pager_Duty

    pager_duty = Pager_Duty.objects.all()

    yaml = render_to_string('alertmanager_template.yml', { 'pager_duty': pager_duty })

    with open(f'/etc/alertmanager/alertmanager.yml', 'w') as file:
        file.write(yaml)
        file.close()

    try:
        response = requests.post('http://alertmanager:9093/-/reload')
        response.raise_for_status()
    except Exception as err:
        raise Exception(f'Error occurred: {err}')
