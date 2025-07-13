from django.forms import ModelForm, URLField, CharField, ValidationError
from .models import Project
from notifications.models import Emails
from availability.models import Service, HTTPCodeService 
from django.conf import settings

class ProjectForm(ModelForm):
     
    url = URLField(help_text="URL must start with http:// or https://")
    scheme = CharField(max_length=5, help_text="URL must start with http:// or https://")

    class Meta:
        model = Project
        fields = ['title', 'url', 'scheme']
    

    # On init we set scheme value with http if url start with https or http if url start with url
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.instance.url:
            if self.instance.url.startswith('https://'):
                self.initial['scheme'] = 'https'
                self.initial['url'] = self.instance.url.replace('https://', '')
            else:
                self.initial['scheme'] = 'http'
                self.initial['url'] = self.instance.url.replace('http://', '')

    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('http://') and not url.startswith('https://'):
            raise ValidationError('URL must start with http:// or https://')
        return url
    
    def save(self, commit=True, user=None):
        url = self.cleaned_data['url'].replace('https://', '').replace('http://', '')
        domain = url
        if self.cleaned_data['scheme'] == 'https':
            url = 'https://' + url
        else:
            url = 'http://' + url

        project = super(ProjectForm, self).save(commit=False)
        project.url = url
        project.save()

        return project

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

        if not self.user.is_superuser and not self.user.is_staff and self.user.projects.count() >= settings.FREEMIUM_PROJECTS:
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
        project.url = url
        project.user = user
        project.save()

        # Lighthouse.objects.create(url=url, project=project)
        service = Service.objects.create(project=project, title=domain)
        HTTPCodeService.objects.create(url=url, service=service)
        Emails.objects.create(project=project, email=user.email)

        return project

