from django.contrib import admin
from .models import Performance, Report, ReportScreenshots

class PerformancesAdmin(admin.ModelAdmin):
    list_display = ('project', 'url', 'last_request_date')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('performance', 'score_performance', 'score_accessibility', 'score_best_practices', 'score_seo', 'score_pwa', 'creation_date')

class ReportScreenshotsAdmin(admin.ModelAdmin):
    list_display = ('report', 'timing', 'timestamp')

admin.site.register(Performance, PerformancesAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportScreenshots, ReportScreenshotsAdmin)
