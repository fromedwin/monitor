from django.contrib import admin
from .models import Lighthouse, Report

class LighthouseAdmin(admin.ModelAdmin):
    list_display = ('page', 'last_request_date')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('performance', 'score_performance', 'score_accessibility', 'score_best_practices', 'score_seo', 'score_pwa', 'has_screenshot', 'has_json', 'creation_date')


    @admin.display(boolean=True)
    def has_screenshot(self, obj):
        return obj.screenshot is not None and obj.screenshot != ""

    @admin.display(boolean=True)
    def has_json(self, obj):
        return obj.report_json_file is not None and obj.report_json_file != ""

admin.site.register(Lighthouse, LighthouseAdmin)
admin.site.register(Report, ReportAdmin)
