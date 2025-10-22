from django.contrib import admin
from .models import Project, Pages, PageLink

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_favorite')

admin.site.register(Project, ProjectAdmin)

class PagesAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'url', 'sitemap_last_seen', 'scraping_last_seen', 'lighthouse_last_request')

admin.site.register(Pages, PagesAdmin)

class PageLinkAdmin(admin.ModelAdmin):
    list_display = ('from_page_title', 'to_page_title', 'from_page_url', 'to_page_url', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'from_page__project')
    search_fields = ('from_page__title', 'to_page__title', 'from_page__url', 'to_page__url')
    raw_id_fields = ('from_page', 'to_page')
    
    def from_page_title(self, obj):
        return obj.from_page.title or "No title"
    from_page_title.short_description = 'From Page Title'
    
    def to_page_title(self, obj):
        return obj.to_page.title or "No title"
    to_page_title.short_description = 'To Page Title'
    
    def from_page_url(self, obj):
        return obj.from_page.url
    from_page_url.short_description = 'From URL'
    
    def to_page_url(self, obj):
        return obj.to_page.url
    to_page_url.short_description = 'To URL'

admin.site.register(PageLink, PageLinkAdmin)
