from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'fromedwin'
    verbose_name = "FromEdwin"

    def ready(self):
        import fromedwin.signals # Load signals
