# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from django.conf import settings
from website.urls import urlpatterns

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"
    protocol = "https" if settings.FORCE_HTTPS else "http"

    def items(self):
        return [pattern.name for pattern in urlpatterns]

    def location(self, item):
        return reverse(item)