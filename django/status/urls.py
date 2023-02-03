from django.urls import path

from .views import public, badge, project_status_public, toggle_public_page

urlpatterns = [
    # Show full status page
    path('status/<int:id>/', public, name='public'),
    # Return mime-type image/svg+xml
    path('status/<int:id>/badge.svg', badge, name='badge'),
    # Manage status page for project id (enable/disable and show badge code)
    path('project/<int:id>/public_status/', project_status_public, name='project_status_public'),
    # enable-diable status page for project id
    path('project/<int:application_id>/toggle_public_page/', toggle_public_page, name='toggle_public_page'),
]
