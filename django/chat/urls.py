from django.urls import path

from .views import messages

urlpatterns = [
    # Administraiton panel for django superuser
    path('', messages, name='messages'),
]
