from django.contrib import admin
from .models import Emails, Notification
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatechars

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('date', 'message_stripped', 'user', 'severity')

    @admin.display()
    def message_stripped(self, obj):
        return truncatechars(strip_tags(obj.message), 50)

    @admin.display()
    def user(self, obj):
        return obj.service.project.user if obj.service else None

class EmailsAdmin(admin.ModelAdmin):
    list_display = ('project', 'email')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Emails, EmailsAdmin)
