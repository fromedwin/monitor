from django.forms import ModelForm
from .models import Application, Service

class ApplicationForm(ModelForm):
	class Meta:
		model = Application
		fields = ['title']