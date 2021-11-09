from django.apps import AppConfig
from clients.config import generate_alert_manager_config

class MyAppConfig(AppConfig):
    name = 'monitor'
    verbose_name = "Monitor"

    def ready(self):

        import monitor.signals # Load signals

        """
        On start, django generate alert anager yml files using data from db 
        and reload alertmanager with http call
        """
        try:
            generate_alert_manager_config()
        except:
            pass