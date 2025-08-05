from django.urls import path

from .views import reports_home, project_reports

urlpatterns = [
    # Reports home page showing list of all reports
    path('reports/', reports_home, name='reports_home'),
    # Project-specific reports page
    path('project/<int:id>/reports/', project_reports, name='project_reports'),
] 