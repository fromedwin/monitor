from django.urls import path

from .api import save_favicon

urlpatterns = [
    # API endpoints for favicon functionality
    path('api/save_favicon/<str:secret_key>/<int:project_id>/', save_favicon, name='save_favicon'),
] 