from django.forms import ModelForm
from .models import Emails

class EmailsForm(ModelForm):
    class Meta:
        model = Emails
        fields = ['email']
