from django.contrib import admin

from .models import ProjectReport


@admin.register(ProjectReport)
class ProjectReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project',
        'status',
        'creation_date',
        'celery_task_log',
    )
    list_select_related = (
        'project',
        'celery_task_log',
    )
    ordering = ('-creation_date',)
    list_filter = ('creation_date',)
    search_fields = (
        'id',
        'project__title',
        'project__url',
    )
    date_hierarchy = 'creation_date'
    readonly_fields = (
        'creation_date',
    )
    raw_id_fields = (
        'project',
        'celery_task_log',
    )

    def status(self, obj):
        try:
            return obj.data.get('status')
        except Exception:
            return None
    status.short_description = 'Status'
