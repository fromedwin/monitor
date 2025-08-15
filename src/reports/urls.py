from django.urls import path

from .views import reports_home, project_reports, report_email_preview
from .api import queue_report_generation

urlpatterns = [
    # Reports home page showing list of all reports
    path('reports/', reports_home, name='reports_home'),
    # Project-specific reports page
    path('project/<int:id>/reports/', project_reports, name='project_reports'),
    # Email preview for a specific report
    path('project/<int:project_id>/reports/<int:report_id>/email-preview/', report_email_preview, name='report_email_preview'),
    # API endpoint for queuing report generation
    path('api/project/<int:project_id>/queue-report/', queue_report_generation, name='queue_report_generation_api'),
] 