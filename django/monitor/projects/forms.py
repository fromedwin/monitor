from django.forms import ModelForm
from .models import Project, Service, HTTPCodeService, HTTPMockedCodeService

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['title']

class ServiceForm(ModelForm):
	class Meta:
		model = Service
		fields = ['title', 'is_public', 'is_enabled','is_critical']

class HTTPCodeServiceForm(ModelForm):
	class Meta:
		model = HTTPCodeService
		fields = ['url']

class MockedHTTPCodeServiceForm(ModelForm):
	class Meta:
		model = HTTPMockedCodeService
		fields = ['code']