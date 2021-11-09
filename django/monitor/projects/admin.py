from django.contrib import admin
from .models import Project, Service

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('project', 'title',  'url', 'is_critical', 'is_enabled', 'is_public')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Service, ServiceAdmin)
