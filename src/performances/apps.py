from django.apps import AppConfig

class PerformancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'performances'

    def ready(self):
        import performances.tasks.queue_deprecated_performance