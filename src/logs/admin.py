from django.contrib import admin
from .models import CeleryTaskLog

# Register your models here.

@admin.register(CeleryTaskLog)
class CeleryTaskLogAdmin(admin.ModelAdmin):
    list_display = ['project','task_name', 'duration', 'created_at']
    list_filter = ['task_name', 'created_at', 'project']
    search_fields = ['task_name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
