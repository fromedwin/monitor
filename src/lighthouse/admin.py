from django.contrib import admin

# Register your models here.
from .models import LighthouseReport

@admin.register(LighthouseReport)
class LighthouseReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'page_url',
        'form_factor',
        'score_performance',
        'score_accessibility',
        'score_best_practices',
        'score_seo',
        'score_pwa',
        'creation_date',
    )
    list_filter = ('form_factor', 'creation_date')
    search_fields = ('page__url',)
    readonly_fields = ('creation_date',)

    def page_url(self, obj):
        return obj.page.url
    page_url.short_description = 'Page URL'
    page_url.admin_order_field = 'page__url'
