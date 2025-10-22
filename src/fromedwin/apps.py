from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'fromedwin'
    verbose_name = "FromEdwin Core"

    def ready(self):
        import fromedwin.signals # Load signals
        import django_celery_beat.schedulers
