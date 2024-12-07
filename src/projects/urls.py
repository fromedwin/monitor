from django.urls import path

from .views import project, projects_form, projects_delete, projects_add, projects_welcome
from incidents.views import incidents
from .api import fetch_deprecated_favicons, fetch_deprecated_sitemaps, save_favicon, save_sitemap, save_scaping

# from .api import fetch_deprecated_favicons, save_favicon

urlpatterns = [
    # Welcome page
    path('welcome/', projects_welcome, name='projects_welcome'),
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
]

#
# Add APIs URL
#
urlpatterns += [
    # 
    path('api/fetch_deprecated_favicons/<str:secret_key>/', fetch_deprecated_favicons, name='fetch_deprecated_favicons'),
    # 
    path('api/fetch_deprecated_sitemaps/<str:secret_key>/', fetch_deprecated_sitemaps, name='fetch_deprecated_sitemaps'),
    # 
    path('api/save_favicon/<str:secret_key>/<int:project_id>/', save_favicon, name='save_favicon'),
    # 
    path('api/save_sitemap/<str:secret_key>/<int:project_id>/', save_sitemap, name='save_sitemap'),
    # 
    path('api/save_scaping/<str:secret_key>/<int:page_id>/', save_scaping, name='save_scaping'),
]

