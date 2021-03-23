from django.contrib import admin
from .models import GenericAlert, InstanceDownAlert

class InstanceDownAlertAdmin(admin.ModelAdmin):
    list_display = ("instance", "status", "startsAt", "endsAt")
    fields = ("status", "severity", "instance", "startsAt", "endsAt", "json")

admin.site.register(InstanceDownAlert, InstanceDownAlertAdmin)

class GenericAlertAdmin(admin.ModelAdmin):
    list_display = ("creation_date", "short_json")

admin.site.register(GenericAlert, GenericAlertAdmin)
