from django.contrib import admin
from .models import Server, Metrics, Alerts, AuthBasic
from django.utils import timezone
import math

class AlertsAdmin(admin.ModelAdmin):
    list_display = ('alert', '__str__')

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

admin.site.register(Alerts, AlertsAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Metrics, MetricsAdmin)
admin.site.register(AuthBasic)
