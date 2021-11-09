from django.urls import path
from .views import pagerduty_form, pagerduty_delete

urlpatterns = [
    path('pagerduty/add', pagerduty_form, name='pagerduty_add'),
    path('pagerduty/<int:pagerduty_id>/edit', pagerduty_form, name='pagerduty_edit'),
    path('pagerduty/<int:pagerduty_id>/delete', pagerduty_delete, name='pagerduty_delete'),
]
