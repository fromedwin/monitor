from django.urls import path

from .views import project_reports, view_report_html, view_report_json, view_report_email
from .api import queue_report_generation, get_report_by_id

urlpatterns = [
    # Project-specific reports page
    path('project/<int:id>/reports/', project_reports, name='project_reports'),
    # API endpoint for queuing report generation
    path('api/project/<int:project_id>/queue-report/', queue_report_generation, name='queue_report_generation_api'),
    # API endpoint for fetching a specific report by ID
    path('api/reports/<int:report_id>/', get_report_by_id, name='get_report_by_id_api'),

    # View a specific report by ID
    path('project/<int:project_id>/reports/reports/<int:report_id>/', view_report_html, name='view_report_html'),
    # View a specific report by ID
    path('project/<int:project_id>/reports/reports/<int:report_id>/json/', view_report_json, name='view_report_json'),
    # View a specific report by ID
    path('project/<int:project_id>/reports/reports/<int:report_id>/email/', view_report_email, name='view_report_email'),
    
] 