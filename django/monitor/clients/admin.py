from django.contrib import admin
from .models import AlertsConfig, PrometheusConfig, Server

class AlertsConfigAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__')

class PrometheusConfigAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__')

class ServerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'uuid', 'last_seen')

admin.site.register(AlertsConfig, AlertsConfigAdmin)
admin.site.register(PrometheusConfig, PrometheusConfigAdmin)
admin.site.register(Server, ServerAdmin)
