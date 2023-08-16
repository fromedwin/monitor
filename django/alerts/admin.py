from django.contrib import admin

from .models import Alerts, AlertsWarning, AlertsCritical, DisableAlerts

# Register your models here.
class AlertsAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_critical',  'has_warning', 'has_critical')

    @admin.display(boolean=True)
    def has_warning(self, obj):
        return bool(obj.warning)

    @admin.display(boolean=True)
    def has_critical(self, obj):
        return bool(obj.critical)

admin.site.register(Alerts, AlertsAdmin)
admin.site.register(AlertsWarning)
admin.site.register(AlertsCritical)
admin.site.register(DisableAlerts)
