from django.urls import path

from .views import projects, project, projects_form, service_http_form, projects_delete, service_list, service_http_delete, service_mockedhttp_form, service_mockedhttp_delete, toggle_public_page, project_availability, project_performances, project_notifications, project_status_public
from alerts.views import incidents

urlpatterns = [
    path('projects/', projects, name='projects'),
    path('project/add', projects_form, name='projects_add'),
    path('project/<int:id>/edit/', projects_form, name='projects_edit'),
    path('project/<int:id>/delete/', projects_delete, name='projects_delete'),
    path('project/<int:id>/', project, name='project'),
    path('project/<int:id>/availability/', project_availability, name='project_availability'),
    path('project/<int:id>/performances/', project_performances, name='project_performances'),
    path('project/<int:id>/notifications/', project_notifications, name='project_notifications'),
    path('project/<int:id>/public_status/', project_status_public, name='project_status_public'),
    path('project/<int:application_id>/toggle_public_page/', toggle_public_page, name='toggle_public_page'),
    path('project/<int:application_id>/services/add', service_list, name='services_add'),
    path('project/<int:application_id>/services/httpcode/add', service_http_form, name='services_httpcode_add'),
    path('project/<int:application_id>/services/httpcode/<int:service_http_id>/edit', service_http_form, name='services_httpcode_edit'),
    path('project/<int:application_id>/services/httpcode/<int:service_http_id>/delete', service_http_delete, name='services_httpcode_delete'),
    path('project/<int:application_id>/services/mockedhttpcode/add', service_mockedhttp_form, name='services_mockedhttpcode_add'),
    path('project/<int:application_id>/services/mockedhttpcode/<int:service_http_id>/edit', service_mockedhttp_form, name='services_mockedhttpcode_edit'),
    path('project/<int:application_id>/services/mockedhttpcode/<int:service_http_id>/delete', service_mockedhttp_delete, name='services_mockedhttpcode_delete'),
    # incidents
    path('project/<int:id>/incidents/', incidents, name='incidents'),
    path('project/<int:id>/incidents/<int:year>/<int:month>/<int:day>/', incidents, name='incidents'),

]
