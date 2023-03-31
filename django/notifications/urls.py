from django.urls import path
from .views import pagerduty_form, pagerduty_delete, project_notifications, email_form, email_delete

urlpatterns = [
    # Show notification panel for project id
    path('project/<int:id>/notifications/', project_notifications, name='project_notifications'),
    # manage pagerduty id for alerts and notifications
    path('project/<int:application_id>/notifications/pagerduty/add', pagerduty_form, name='pagerduty_add'),
    path('project/<int:application_id>/notifications/pagerduty/<int:pagerduty_id>/edit', pagerduty_form, name='pagerduty_edit'),
    path('project/<int:application_id>/notifications/pagerduty/<int:pagerduty_id>/delete', pagerduty_delete, name='pagerduty_delete'),
    # manage pagerduty id for alerts and notifications
    path('project/<int:application_id>/notifications/emails/add', email_form, name='email_add'),
    path('project/<int:application_id>/notifications/emails/<int:email_id>/edit', email_form, name='email_edit'),
    path('project/<int:application_id>/notifications/emails/<int:email_id>/delete', email_delete, name='email_delete'),
]
