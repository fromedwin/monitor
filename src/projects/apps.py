from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

    def ready(self):
        import projects.signals # Load signals
        import projects.tasks.fetch_favicon
        import projects.tasks.queue_deprecated_favicons