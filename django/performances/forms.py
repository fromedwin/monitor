from django.forms import ModelForm
from .models import Performance

class PerformanceForm(ModelForm):
    class Meta:
        model = Performance
        fields = ['url']
