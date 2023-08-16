from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'core'
    verbose_name = "FromEdwin Core"

    def ready(self):
        import core.signals # Load signals
