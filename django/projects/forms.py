from django.forms import ModelForm, URLField, CharField, ValidationError
from .models import Project
from performances.models import Performance
from notifications.models import Emails
from availability.models import Service, HTTPCodeService 
from django.conf import settings

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['title', 'is_favorite']

class ProjectCreateForm(ModelForm):

    # Django form expecting a URLFirld
    url = URLField(help_text="URL must start with http:// or https://")
    scheme = CharField(max_length=5, help_text="URL must start with http:// or https://")

    class Meta:
        model = Project
        fields = ['url', 'scheme']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    # Define clean method to raise Validation error if user has more than 3 projects
    def clean(self):
        cleaned_data = super(ProjectCreateForm, self).clean()
        if self.user.applications.count() >= settings.FREEMIUM_PROJECTS:
            raise ValidationError(f'You can only have {settings.FREEMIUM_PROJECTS} projects')
        return cleaned_data

    # Define clean_url method to raise Validation error if url does not start with http:// or https://

    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('http://') and not url.startswith('https://'):
            raise ValidationError('URL must start with http:// or https://')
        return url

    # Override save method to save the project title with the url value
    def save(self, commit=True, user=None):

        # If user is None then throw an exception to fail the save
        if not user:
            raise Exception('User is required')

        url = self.cleaned_data['url'].replace('https://', '').replace('http://', '')
        domain = url
        if self.cleaned_data['scheme'] == 'https':
            url = 'https://' + url
        else:
            url = 'http://' + url

        project = super(ProjectCreateForm, self).save(commit=False)
        project.title = domain
        project.user = user
        project.save()

        performance = Performance.objects.create(url=url, project=project)
        service = Service.objects.create(project=project, title=domain)
        availability = HTTPCodeService.objects.create(url=url, service=service)
        email = Emails.objects.create(project=project, email=user.email)

        return project

