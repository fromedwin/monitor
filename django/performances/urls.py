from django.urls import path

from .api import fetch_performance, save_report
from .views import project_performances, performance_form, performance_delete, project_performances_report_viewer

urlpatterns = [
    # Display performances panel
    path('project/<int:id>/performances/', project_performances, name='project_performances'),
    # Display performances panel
    path('project/<int:id>/performances/report/<int:report_id>', project_performances_report_viewer, name='project_performances_report_viewer'),
    # Manage httpcode object, aka url to track
    path('project/<int:application_id>/performance/add', performance_form, name='performance_add'),
    path('project/<int:application_id>/performance/<int:performance_id>/edit', performance_form, name='performance_edit'),
    path('project/<int:application_id>/performance/<int:performance_id>/delete', performance_delete, name='performance_delete'),

    # As a server, return the next performance url to run
    path('api/request/<uuid:server_id>/performance', fetch_performance, name='fetch_performance'),
    # Report lighthouse performance
    path('api/report/<uuid:server_id>/performance/<int:performance_id>', save_report, name='fetch_performance'),
    
]
