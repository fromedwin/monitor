from django.contrib import admin
from .models import Incident, UnknownIncident, ServiceIncident

class IncidentAdmin(admin.ModelAdmin):
    list_display = ("starts_at", "ends_at", "status", "severity")

class UnknownIncidentAdmin(admin.ModelAdmin):
    list_display = ("alert_name", "summary", "description")

class ServiceIncidentAdmin(admin.ModelAdmin):
    list_display = ("incident", "service", "alert")

admin.site.register(Incident, IncidentAdmin)
admin.site.register(UnknownIncident, UnknownIncidentAdmin)
admin.site.register(ServiceIncident, ServiceIncidentAdmin)

