from django.urls import path

from .views import project_availability, service_list, service_http_form, service_http_form, service_http_delete, service_mockedhttp_form, service_mockedhttp_form, service_mockedhttp_delete, healthy

urlpatterns = [
    # Healthy API called by API to MockedHTTP
    path('healthy/<int:id>/', healthy, name='healthy'),
    # Show availability overview for project
    path('project/<int:id>/availability/', project_availability, name='project_availability'),
    # List of service available for availability
    path('project/<int:application_id>/availability/add', service_list, name='services_add'),
    # Manage httpcode object, aka url to track
    path('project/<int:application_id>/availability/httpcode/add', service_http_form, name='services_httpcode_add'),
    path('project/<int:application_id>/availability/httpcode/<int:service_http_id>/edit', service_http_form, name='services_httpcode_edit'),
    path('project/<int:application_id>/availability/httpcode/<int:service_http_id>/delete', service_http_delete, name='services_httpcode_delete'),
    # Manage fake url to track for testing purpose
    path('project/<int:application_id>/availability/mockedhttpcode/add', service_mockedhttp_form, name='services_mockedhttpcode_add'),
    path('project/<int:application_id>/availability/mockedhttpcode/<int:service_http_id>/edit', service_mockedhttp_form, name='services_mockedhttpcode_edit'),
    path('project/<int:application_id>/availability/mockedhttpcode/<int:service_http_id>/delete', service_mockedhttp_delete, name='services_mockedhttpcode_delete'),

]
