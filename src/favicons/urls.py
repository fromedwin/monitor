from django.urls import path

from .api import fetch_deprecated_favicons, save_favicon

urlpatterns = [
    # API endpoints for favicon functionality
    path('api/fetch_deprecated_favicons/<str:secret_key>/', fetch_deprecated_favicons, name='fetch_deprecated_favicons'),
    path('api/save_favicon/<str:secret_key>/<int:project_id>/', save_favicon, name='save_favicon'),
] 