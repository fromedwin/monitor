from django.urls import path

from .views import administration, test_email

urlpatterns = [
    # Administraiton panel for django superuser
    path('', administration, name='administration'),
    path('test_email/', test_email, name='test_email'),
]
