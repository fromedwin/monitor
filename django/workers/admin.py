from django.contrib import admin
from .models import Server, Metrics, Alerts, AuthBasic
from django.utils import timezone
import math

class AlertsAdmin(admin.ModelAdmin):
    list_display = ('alert', '__str__')

class ServerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user',  'is_public', 'uuid', 'has_auth_basic', 'is_active', 'performance', 'monitoring', 'last_seen_duration')

    @admin.display(boolean=True)
    def has_auth_basic(self, obj):
        return len(obj.authbasic.all()) != 0

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

class AuthBasicAdmin(admin.ModelAdmin):

    def server_name(self, obj):
        return str(obj.server.id) + ' - ' + str(obj.server.ip) + ' - ' + str(obj.server.uuid)
    list_display = ('server_name', 'username', 'password')

admin.site.register(Alerts, AlertsAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Metrics, MetricsAdmin)
admin.site.register(AuthBasic, AuthBasicAdmin)
