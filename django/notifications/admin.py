from django.contrib import admin
from .models import Emails, Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('date', 'severity')

class EmailsAdmin(admin.ModelAdmin):
    list_display = ('project', 'email')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Emails, EmailsAdmin)
