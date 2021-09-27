from django.contrib import admin
from .models import Application, Service

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'enable_public_status')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('application', 'title',  'url', 'is_public')

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Service, ServiceAdmin)
