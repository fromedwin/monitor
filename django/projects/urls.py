from django.urls import path

from .views import projects, project, projects_form, projects_delete, toggle_public_page, project_performances, project_notifications, project_status_public
from alerts.views import incidents

urlpatterns = [
    path('projects/', projects, name='projects'),
    path('project/add', projects_form, name='projects_add'),
    path('project/<int:id>/edit/', projects_form, name='projects_edit'),
    path('project/<int:id>/delete/', projects_delete, name='projects_delete'),
    path('project/<int:id>/', project, name='project'),
    path('project/<int:id>/performances/', project_performances, name='project_performances'),
    path('project/<int:id>/notifications/', project_notifications, name='project_notifications'),
    path('project/<int:id>/public_status/', project_status_public, name='project_status_public'),
    path('project/<int:application_id>/toggle_public_page/', toggle_public_page, name='toggle_public_page'),
    # incidents
    path('project/<int:id>/incidents/', incidents, name='incidents'),
    path('project/<int:id>/incidents/<int:year>/<int:month>/<int:day>/', incidents, name='incidents'),

]
