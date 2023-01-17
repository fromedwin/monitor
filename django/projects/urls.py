from django.urls import path

from .views import projects, project, projects_form, service_http_form, projects_delete, service_list, service_http_delete, service_mockedhttp_form, service_mockedhttp_delete, toggle_public_page
from alerts.views import incidents

urlpatterns = [
    path('', projects, name='projects'),
    path('add', projects_form, name='projects_add'),
    path('<int:id>/edit/', projects_form, name='projects_edit'),
    path('<int:id>/delete/', projects_delete, name='projects_delete'),
    path('<int:id>/', project, name='project'),
    path('<int:application_id>/toggle_public_page/', toggle_public_page, name='toggle_public_page'),
    path('<int:application_id>/services/add', service_list, name='services_add'),
    path('<int:application_id>/services/httpcode/add', service_http_form, name='services_httpcode_add'),
    path('<int:application_id>/services/httpcode/<int:service_http_id>/edit', service_http_form, name='services_httpcode_edit'),
    path('<int:application_id>/services/httpcode/<int:service_http_id>/delete', service_http_delete, name='services_httpcode_delete'),
    path('<int:application_id>/services/mockedhttpcode/add', service_mockedhttp_form, name='services_mockedhttpcode_add'),
    path('<int:application_id>/services/mockedhttpcode/<int:service_http_id>/edit', service_mockedhttp_form, name='services_mockedhttpcode_edit'),
    path('<int:application_id>/services/mockedhttpcode/<int:service_http_id>/delete', service_mockedhttp_delete, name='services_mockedhttpcode_delete'),
    # incidents
    path('<int:id>/incidents/', incidents, name='incidents'),
    path('<int:id>/incidents/<int:year>/<int:month>/<int:day>/', incidents, name='incidents'),

]
