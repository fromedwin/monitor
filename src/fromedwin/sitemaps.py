# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from django.conf import settings
from website.urls import urlpatterns

class StaticViewSitemap(sitemaps.Sitemap):
    """
    Generate a sitemap for static views used in public website.
    """
    priority = 0.5
    changefreq = "weekly"
    protocol = "https" if settings.FORCE_HTTPS else "http"

    def items(self):
        """
        Returns a list of URL pattern names from the project's urlpatterns.
        These names are used to generate the sitemap entries.
        """
        return [pattern.name for pattern in urlpatterns]

    def location(self, item):
        """
        Returns the full URL for a given URL pattern name.
        """
        return reverse(item)