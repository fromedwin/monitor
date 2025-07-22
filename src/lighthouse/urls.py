from django.urls import path

from .api import report_api, fetch_deprecated_performances, report_json_api
from .views import project_pages_report_viewer

urlpatterns = [
    # Display performances panel
    path('project/<int:id>/pages/report/<int:report_id>', project_pages_report_viewer, name='project_pages_report_viewer'),
]

#
# Add APIs URL
#
urlpatterns += [
    # Return id and url for performances to fetch
    path('api/fetch_deprecated_performances/<str:secret_key>/', fetch_deprecated_performances, name='fetch_deprecated_performances'),
    # Report lighthouse performance
    path('api/report/<str:secret_key>/performance/<int:page_id>', report_api, name='save_report'),
    # Get lighthouse report JSON data
    path('api/report/<int:report_id>/json/', report_json_api, name='report_json_api'),
]