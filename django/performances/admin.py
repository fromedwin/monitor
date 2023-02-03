from django.contrib import admin
from .models import Performance, Report, ReportScreenshots

class PerformancesAdmin(admin.ModelAdmin):
    list_display = ('project', 'url', 'last_request_date')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('performance', 'score_performance', 'score_accessibility', 'score_best_practices', 'score_seo', 'score_pwa', 'has_screenshot', 'has_json', 'creation_date')


    @admin.display(boolean=True)
    def has_screenshot(self, obj):
        return obj.screenshot is not None and obj.screenshot != ""

    @admin.display(boolean=True)
    def has_json(self, obj):
        return obj.report_json_file is not None and obj.report_json_file != ""

class ReportScreenshotsAdmin(admin.ModelAdmin):
    list_display = ('report', 'timing', 'timestamp')

admin.site.register(Performance, PerformancesAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportScreenshots, ReportScreenshotsAdmin)
