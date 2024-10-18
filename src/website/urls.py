from django.urls import path
from .views import homepage, pricing, features, legal, aboutus

urlpatterns = [
    # Main homepage with coming soon message
    path('', homepage, name='homepage'),
    path('pricing', pricing, name='pricing'),
    path('features', features, name='features'),
    path('about-us', aboutus, name='about-us'),
    path('legal', legal, name='legal'),
]