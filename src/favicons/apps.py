from django.apps import AppConfig


class FaviconsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "favicons"

    def ready(self):
        import favicons.tasks