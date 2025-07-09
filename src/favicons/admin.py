from django.contrib import admin
from .models import Favicon


@admin.register(Favicon)
class FaviconAdmin(admin.ModelAdmin):
    """Admin configuration for Favicon model"""
    list_display = ('project', 'task_status', 'last_edited', 'created_at')
    list_filter = ('task_status', 'created_at', 'last_edited')
    search_fields = ('project__title', 'project__user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Project Information', {
            'fields': ('project',)
        }),
        ('Favicon Details', {
            'fields': ('favicon', 'task_status', 'last_edited')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
