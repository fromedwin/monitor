from django.apps import AppConfig
from clients.config import generate_alert_manager_config

class MyAppConfig(AppConfig):
    name = 'monitor'
    verbose_name = "Monitor"
    def ready(self):
        try:
            generate_alert_manager_config()
        except:
            pass