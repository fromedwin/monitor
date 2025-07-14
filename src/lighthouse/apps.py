from django.apps import AppConfig


class LighthouseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lighthouse"

    def ready(self):
        import lighthouse.tasks.queue_deprecated_performance
