from django.contrib import admin
from .models import GenericIncident, ProjectIncident, InstanceDownIncident

class InstanceDownIncidentAdmin(admin.ModelAdmin):
    list_display = ("instance", "severity", "status", "startsAt", "endsAt", "duration")
    fields = ("service", "status", "severity", "instance", "startsAt", "endsAt", "json")

admin.site.register(InstanceDownIncident,InstanceDownIncidentAdmin)

class ProjectAlertAdmin(admin.ModelAdmin):
    list_display = ("instance", "status", "startsAt", "endsAt", "duration")
    fields = ("project", "status", "severity", "instance", "startsAt", "endsAt", "json")

admin.site.register(ProjectIncident, ProjectAlertAdmin)

class GenericIncidentAdmin(admin.ModelAdmin):
    fields = ("status", "severity", "instance", "startsAt", "endsAt", "json")
    list_display = ("summary", "status", "startsAt", "endsAt", "duration")

admin.site.register(GenericIncident, GenericIncidentAdmin)

