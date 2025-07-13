from django.urls import path

from .api import report_api, fetch_deprecated_performances

# urlpatterns = [
#     # Display performances panel
#     path('project/<int:id>/performances/', project_performances, name='project_performances'),
#     # Display performances panel
#     path('project/<int:id>/performances/report/<int:report_id>', project_performances_report_viewer, name='project_performances_report_viewer'),
# ]

#
# Add APIs URL
#
urlpatterns = [
    # Return id and url for performances to fetch
    path('api/fetch_deprecated_performances/<str:secret_key>/', fetch_deprecated_performances, name='fetch_deprecated_performances'),
    # Report lighthouse performance
    path('api/report/<str:secret_key>/performance/<int:page_id>', report_api, name='save_report'),
]