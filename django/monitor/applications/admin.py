from django.contrib import admin
from .models import Application, Service, Metrics

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'enable_public_status')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('application', 'title',  'url', 'is_public')

class MetricsAdmin(admin.ModelAdmin):
    list_display = ('user', 'url')

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Metrics, MetricsAdmin)
