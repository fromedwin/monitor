from django.urls import path

from .views import incidents_force_online

urlpatterns = [
    # Delete all open incidents regarding service_id for project_id
    path('services/<int:service_id>/close_incidents/', incidents_force_online, name='incidents_close_firing'),
    path('services/<int:service_id>/delete_incidents/', incidents_force_online, name='incidents_delete_firing'),

]
