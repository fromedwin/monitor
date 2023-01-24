from django.urls import path

from .views import project_availability, service_list, service_http_form, service_http_form, service_http_delete, service_mockedhttp_form, service_mockedhttp_form, service_mockedhttp_delete

urlpatterns = [
    path('project/<int:id>/availability/', project_availability, name='project_availability'),
    path('project/<int:application_id>/services/add', service_list, name='services_add'),
    path('project/<int:application_id>/services/httpcode/add', service_http_form, name='services_httpcode_add'),
    path('project/<int:application_id>/services/httpcode/<int:service_http_id>/edit', service_http_form, name='services_httpcode_edit'),
    path('project/<int:application_id>/services/httpcode/<int:service_http_id>/delete', service_http_delete, name='services_httpcode_delete'),
    path('project/<int:application_id>/services/mockedhttpcode/add', service_mockedhttp_form, name='services_mockedhttpcode_add'),
    path('project/<int:application_id>/services/mockedhttpcode/<int:service_http_id>/edit', service_mockedhttp_form, name='services_mockedhttpcode_edit'),
    path('project/<int:application_id>/services/mockedhttpcode/<int:service_http_id>/delete', service_mockedhttp_delete, name='services_mockedhttpcode_delete'),

]
