from django.urls import path
from .views import pagerduty_form, pagerduty_delete, project_notifications

urlpatterns = [
    # Show notification panel for project id
    path('project/<int:id>/notifications/', project_notifications, name='project_notifications'),
    # manage pagerduty id for alerts and notifications
    path('projects/<int:application_id>/notifications/pagerduty/add', pagerduty_form, name='pagerduty_add'),
    path('projects/<int:application_id>/notifications/pagerduty/<int:pagerduty_id>/edit', pagerduty_form, name='pagerduty_edit'),
    path('projects/<int:application_id>/notifications/pagerduty/<int:pagerduty_id>/delete', pagerduty_delete, name='pagerduty_delete'),
]
