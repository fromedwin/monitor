from django.contrib import admin
from .models import Service, HTTPCodeService

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'is_public', 'is_enabled', 'is_critical', 'creation_date',)

class HTTPCodeServiceAdmin(admin.ModelAdmin):
    list_display = ('url', 'service')

admin.site.register(Service, ServiceAdmin)
admin.site.register(HTTPCodeService, HTTPCodeServiceAdmin)