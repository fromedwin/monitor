from django.urls import path

from .views import public, badge, project_status_public, toggle_public_page

urlpatterns = [
    path('status/<int:id>/', public, name='public'),
    path('status/<int:id>/badge.svg', badge, name='badge'),
    path('project/<int:id>/public_status/', project_status_public, name='project_status_public'),
    path('project/<int:application_id>/toggle_public_page/', toggle_public_page, name='toggle_public_page'),
]
