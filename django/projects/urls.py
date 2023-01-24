from django.urls import path

from .views import projects, project, projects_form, projects_delete
from alerts.views import incidents

urlpatterns = [
    path('projects/', projects, name='projects'),
    path('project/add', projects_form, name='projects_add'),
    path('project/<int:id>/edit/', projects_form, name='projects_edit'),
    path('project/<int:id>/delete/', projects_delete, name='projects_delete'),
    path('project/<int:id>/', project, name='project'),
    # incidents
    path('project/<int:id>/incidents/', incidents, name='incidents'),
    path('project/<int:id>/incidents/<int:year>/<int:month>/<int:day>/', incidents, name='incidents'),

]
