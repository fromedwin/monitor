from django.contrib import admin
from .models import Incident

class IncidentAdmin(admin.ModelAdmin):
    list_display = ("alert_name", "starts_at", "ends_at", "status", "severity")

admin.site.register(Incident, IncidentAdmin)
