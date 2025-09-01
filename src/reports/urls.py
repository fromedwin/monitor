from django.urls import path

from .views import project_reports, report_email_preview, view_report
from .api import queue_report_generation, get_report_by_id

urlpatterns = [
    # Project-specific reports page
    path('project/<int:id>/reports/', project_reports, name='project_reports'),
    # Email preview for a specific report
    path('project/<int:project_id>/reports/<int:report_id>/email-preview/', report_email_preview, name='report_email_preview'),
    # View a specific report by ID
    path('project/<int:project_id>/reports/reports/<int:report_id>/', view_report, name='view_report'),
    # API endpoint for queuing report generation
    path('api/project/<int:project_id>/queue-report/', queue_report_generation, name='queue_report_generation_api'),
    # API endpoint for fetching a specific report by ID
    path('api/reports/<int:report_id>/', get_report_by_id, name='get_report_by_id_api'),
    
] 