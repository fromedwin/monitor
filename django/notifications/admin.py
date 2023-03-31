from django.contrib import admin
from .models import Pager_Duty, Emails

class PagerDutyAdmin(admin.ModelAdmin):
    list_display = ('project', 'routing_key')

class EmailsAdmin(admin.ModelAdmin):
    list_display = ('project', 'email')

admin.site.register(Pager_Duty, PagerDutyAdmin)
admin.site.register(Emails, EmailsAdmin)
