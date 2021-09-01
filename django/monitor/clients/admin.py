from django.contrib import admin
from .models import AlertsConfig, PrometheusConfig

class AlertsConfigAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__')

class PrometheusConfigAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__')

admin.site.register(AlertsConfig, AlertsConfigAdmin)
admin.site.register(PrometheusConfig, PrometheusConfigAdmin)
