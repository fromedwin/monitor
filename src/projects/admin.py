from django.contrib import admin
from .models import Project, Pages

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_favorite')

admin.site.register(Project, ProjectAdmin)

class PagesAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'url', 'sitemap_last_seen', 'scraping_last_seen')

admin.site.register(Pages, PagesAdmin)
