from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

    def ready(self):
        import projects.signals # Load signals
        import projects.tasks.fetch_sitemap
        import projects.tasks.queue_deprecated_sitemaps
        import projects.tasks.scrape_page