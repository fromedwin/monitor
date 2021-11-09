from django.urls import path

from .views import projects, project, projects_form, service_form, projects_delete, service_delete

urlpatterns = [
    path('', projects, name='projects'),
    path('add', projects_form, name='projects_add'),
    path('<int:id>/edit/', projects_form, name='projects_edit'),
    path('<int:id>/delete/', projects_delete, name='projects_delete'),
    path('<int:id>/', project, name='project'),
    path('<int:application_id>/services/add', service_form, name='services_add'),
    path('<int:application_id>/services/<int:service_id>/edit', service_form, name='services_edit'),
    path('<int:application_id>/services/<int:service_id>/delete', service_delete, name='services_delete'),

]
