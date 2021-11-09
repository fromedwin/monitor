from django.contrib import admin
from .models import Pager_Duty

class PagerDutyAdmin(admin.ModelAdmin):
    list_display = ('project', 'routing_key')

admin.site.register(Pager_Duty, PagerDutyAdmin)
