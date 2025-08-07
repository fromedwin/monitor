from django.urls import path

from .views import reports_home, project_reports
from .api import fetch_projects_needing_reports, save_report

urlpatterns = [
    # Reports home page showing list of all reports
    path('reports/', reports_home, name='reports_home'),
    # Project-specific reports page
    path('project/<int:id>/reports/', project_reports, name='project_reports'),
    # API endpoint to fetch projects needing reports
    path('api/fetch_projects_needing_reports/<str:secret_key>/', fetch_projects_needing_reports, name='fetch_projects_needing_reports'),
    # API endpoint to save generated reports
    path('api/save_project_report/<str:secret_key>/<int:project_id>/', save_report, name='save_project_report'),
] 