from django.urls import path

from .views import project, projects_form, projects_delete, projects_add, project_graph_tree
from incidents.views import incidents
from .api import fetch_deprecated_sitemaps, save_sitemap, save_scaping, project_pages_tree_json, delete_page

urlpatterns = [
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
    path('project/<int:id>/incidents/<int:year>/<int:month>/<int:day>/', incidents, name='incidents_date'),

    # Show project overview
    path('project/<int:id>/graph/tree/', project_graph_tree, name='project_graph_tree'),
]

#
# Add APIs URL
#
urlpatterns += [
    # 
    path('api/fetch_deprecated_sitemaps/<str:secret_key>/', fetch_deprecated_sitemaps, name='fetch_deprecated_sitemaps'),
    # 
    path('api/save_sitemap/<str:secret_key>/<int:project_id>/', save_sitemap, name='save_sitemap'),
    # 
    path('api/save_scaping/<str:secret_key>/<int:page_id>/', save_scaping, name='save_scaping'),
    # API endpoint to get project pages tree in JSON format
    path('api/project/<int:project_id>/pages/tree/', project_pages_tree_json, name='project_pages_tree_json'),
    # API endpoint to delete a page
    path('api/page/<int:page_id>/delete/', delete_page, name='delete_page'),
]

