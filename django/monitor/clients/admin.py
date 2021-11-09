from django.contrib import admin
from .models import AlertsConfig, Server, Metrics
from django.utils import timezone
import math

class AlertsConfigAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__')

class ServerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user',  'is_public', 'uuid', 'is_active', 'last_seen_duration')

    @admin.display(boolean=True)
    def is_active(self, obj):
        return obj.is_active

    @admin.display(boolean=True)
    def is_public(self, obj):
        return obj.is_public

    def last_seen_duration(self, obj):
        return obj.last_seen_from

class MetricsAdmin(admin.ModelAdmin):
    list_display = ('user', 'url')

admin.site.register(AlertsConfig, AlertsConfigAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Metrics, MetricsAdmin)