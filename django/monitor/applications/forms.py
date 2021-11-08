from django.forms import ModelForm
from .models import Application, Service

class ApplicationForm(ModelForm):
	class Meta:
		model = Application
		fields = ['title']

class ServiceForm(ModelForm):
	class Meta:
		model = Service
		fields = ['title', 'url', 'is_public', 'is_enabled', 'is_critical']