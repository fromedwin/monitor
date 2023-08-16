from django.contrib import admin

from .models import Alerts

# Register your models here.
class AlertsAdmin(admin.ModelAdmin):
    list_display = ('alert', '__str__')

admin.site.register(Alerts, AlertsAdmin)
