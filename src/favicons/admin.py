from django.contrib import admin
from .models import Favicon
from logs.models import CeleryTaskLog


@admin.register(Favicon)
class FaviconAdmin(admin.ModelAdmin):
    """Admin configuration for Favicon model"""
    list_display = ('project', 'task_status', 'last_edited', 'created_at', 'log_duration', 'log_created_at')
    list_filter = ('task_status', 'created_at', 'last_edited')
    search_fields = ('project__title', 'project__user__username')
    readonly_fields = ('created_at', 'updated_at', 'log_duration', 'log_created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Project Information', {
            'fields': ('project',)
        }),
        ('Favicon Details', {
            'fields': ('favicon', 'task_status', 'last_edited')
        }),
        ('Task Log Information', {
            'fields': ('log_duration', 'log_created_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def log_duration(self, obj):
        """Get duration from the latest CeleryTaskLog for this favicon's project"""
        try:
            log = CeleryTaskLog.objects.filter(
                task_name='favicon_task',
                project_id=obj.project_id
            ).order_by('-created_at').first()
            
            if log and log.duration:
                return log.duration
            return "-"
        except Exception:
            return "-"
    log_duration.short_description = 'Task Duration'
    
    def log_created_at(self, obj):
        """Get created_at from the latest CeleryTaskLog for this favicon's project"""
        try:
            log = CeleryTaskLog.objects.filter(
                task_name='favicon_task',
                project_id=obj.project_id
            ).order_by('-created_at').first()
            
            if log:
                return log.created_at
            return "-"
        except Exception:
            return "-"
    log_created_at.short_description = 'Task Created At'
