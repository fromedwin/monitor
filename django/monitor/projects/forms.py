from django.forms import ModelForm
from .models import Project, Service

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['title']

class ServiceForm(ModelForm):
	class Meta:
		model = Service
		fields = ['title', 'url', 'is_public', 'is_enabled', 'is_critical']