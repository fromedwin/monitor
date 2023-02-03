from django.urls import path

from .views import administration

urlpatterns = [
    # Administraiton panel for django superuser
    path('', administration, name='administration'),
]
