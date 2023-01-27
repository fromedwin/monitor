from django.contrib import admin
from .models import Performance

class PerformancesAdmin(admin.ModelAdmin):
    list_display = ('project', 'url', 'last_request_date')

admin.site.register(Performance, PerformancesAdmin)
