from django.urls import path

from .views import project_performances

urlpatterns = [
    path('project/<int:id>/performances/', project_performances, name='project_performances'),
]
