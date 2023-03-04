from django.urls import path

from .views import projects, project, projects_form, projects_delete, projects_add
from alerts.views import incidents

urlpatterns = [
    # List of all projects
    path('projects/', projects, name='projects'),
    # Add form to create a new project
    path('project/add', projects_add, name='projects_add'),
    # Show project overview
    path('project/<int:id>/', project, name='project'),
    # Edit existing project
    path('project/<int:id>/edit/', projects_form, name='projects_edit'),
    # Delete existing project
    path('project/<int:id>/delete/', projects_delete, name='projects_delete'),
    # List of all incidents
    path('project/<int:id>/incidents/', incidents, name='incidents'),
    # List of all incidents with date filter for a specific day
    path('project/<int:id>/incidents/<int:year>/<int:month>/<int:day>/', incidents, name='incidents'),

]
