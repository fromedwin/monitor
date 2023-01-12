from django.apps import AppConfig

class ClientsConfig(AppConfig):
    name = 'workers'

    def ready(self):
        import workers.signals # Load signals
