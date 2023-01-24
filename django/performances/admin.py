from django.contrib import admin
from .models import Performance

class PerformancesAdmin(admin.ModelAdmin):
    list_display = ('project', 'url')

admin.site.register(Performance, PerformancesAdmin)
