from django.urls import path
from .views import homepage

urlpatterns = [
    # Main homepage with coming soon message
    path('', homepage, name='homepage'),
]
