from django.contrib import admin
from .models import GenericAlert, ApplicationAlert, InstanceDownAlert

class InstanceDownAlertAdmin(admin.ModelAdmin):
    list_display = ("instance", "status", "startsAt", "endsAt", "duration")
    fields = ("service", "status", "severity", "instance", "startsAt", "endsAt", "json")

admin.site.register(InstanceDownAlert, InstanceDownAlertAdmin)

class ApplicationAlertAdmin(admin.ModelAdmin):
    list_display = ("instance", "status", "startsAt", "endsAt", "duration")
    fields = ("application", "status", "severity", "instance", "startsAt", "endsAt", "json")

admin.site.register(ApplicationAlert, ApplicationAlertAdmin)

class GenericAlertAdmin(admin.ModelAdmin):
    fields = ("status", "severity", "instance", "startsAt", "endsAt", "json")
    list_display = ("summary", "status", "startsAt", "endsAt", "duration")

admin.site.register(GenericAlert, GenericAlertAdmin)

