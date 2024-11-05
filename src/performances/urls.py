from django.urls import path

from .api import report_api, fetch_deprecated_performances
from .views import performances_all, project_performances, performance_form, performance_delete, project_performances_report_viewer, performance_rerun

urlpatterns = [
    # Display performances panel
    path('performances/', performances_all, name='performances_all'),
    # Display performances panel
    path('project/<int:id>/performances/', project_performances, name='project_performances'),
    # Display performances panel
    path('project/<int:id>/performances/report/<int:report_id>', project_performances_report_viewer, name='project_performances_report_viewer'),
    # Manage httpcode object, aka url to track
    path('project/<int:application_id>/performances/add', performance_form, name='performance_add'),
    path('project/<int:application_id>/performances/<int:performance_id>/edit', performance_form, name='performance_edit'),
    path('project/<int:application_id>/performances/<int:performance_id>/delete', performance_delete, name='performance_delete'),
    path('project/<int:application_id>/performances/<int:performance_id>/rerun', performance_rerun, name='performance_rerun'),

]

#
# Add APIs URL
#
urlpatterns += [
    # Return id and url for performances to fetch
    path('api/fetch_deprecated_performances/<str:secret_key>/', fetch_deprecated_performances, name='fetch_deprecated_performances'),
    # Report lighthouse performance
    path('api/report/<str:secret_key>/performance/<int:performance_id>', report_api, name='save_report'),
]