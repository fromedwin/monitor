from django.contrib import admin
from .models import Alert

class AlertAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'user')

admin.site.register(Alert, AlertAdmin)
