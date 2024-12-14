from django.forms import ModelForm
from .models import Profile

class TimeZoneForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['timezone']
