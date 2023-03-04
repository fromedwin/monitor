from django.forms import ModelForm, URLField
from .models import Project
from performances.models import Performance
from availability.models import Service, HTTPCodeService 

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['title', 'is_favorite']

class ProjectCreateForm(ModelForm):

    # Django form expecting a URLFirld
    url = URLField()

    class Meta:
        model = Project
        fields = ['url']

    # Clean url value on submit form by checking and adding https:// if missing
    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        return url

    # Override save method to save the project title with the url value
    def save(self, commit=True, user=None):

        # If user is None then throw an exception to fail the save
        if not user:
            raise Exception('User is required')

        url = self.cleaned_data['url']

        project = super(ProjectCreateForm, self).save(commit=False)
        project.title = url.replace('https://', '').replace('http://', '')
        project.user = user
        project.save()

        performance = Performance.objects.create(url=url, project=project)
        service = Service.objects.create(project=project, title="Website")
        availability = HTTPCodeService.objects.create(url=url, service=service)

        return project

