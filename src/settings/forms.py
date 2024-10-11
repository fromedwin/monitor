from django.forms import ModelForm, URLField, CharField, BooleanField, ValidationError
from .models import Profile
from django.conf import settings

class TimeZoneForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['timezone']
