from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'monitor'
    verbose_name = "Monitor"

    def ready(self):
        import monitor.signals # Load signals
