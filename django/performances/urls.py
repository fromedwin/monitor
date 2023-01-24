from django.urls import path

from .views import project_performances

urlpatterns = [
    # Display performances panel
    path('project/<int:id>/performances/', project_performances, name='project_performances'),
]
