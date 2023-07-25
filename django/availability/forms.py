from django.forms import ModelForm, URLField, CharField, BooleanField, ValidationError
from .models import Service, HTTPCodeService, HTTPMockedCodeService
from django.conf import settings

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'is_public', 'is_enabled','is_critical']

class HTTPCodeServiceForm(ModelForm):

    url = URLField(help_text="URL must start with http:// or https://")
    scheme = CharField(max_length=5, help_text="URL must start with http:// or https://")
    tls_skip_verify = BooleanField(label="Disable fail on unsecure SSL", required=False, help_text="Might be needed when you do not fully control the hosting (often cdn or object storage)")

    class Meta:
        model = HTTPCodeService
        fields = ['url', 'scheme', 'tls_skip_verify']

    # On init we set scheme value with http if url start with https or http if url start with url
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super(HTTPCodeServiceForm, self).__init__(*args, **kwargs)
        if self.instance.url:
            if self.instance.url.startswith('https://'):
                self.initial['scheme'] = 'https'
                self.initial['url'] = self.instance.url.replace('https://', '')
            else:
                self.initial['scheme'] = 'http'
                self.initial['url'] = self.instance.url.replace('http://', '')

    # Define clean method to raise Validation error if user has more than 3 projects
    def clean(self):
        cleaned_data = super(HTTPCodeServiceForm, self).clean()
        # If there is more HTTPCodeService with service.project equal to self.project
        # we raise a validation error
        if not self.project.user.is_superuser and not self.project.user.is_staff and not self.instance.pk and HTTPCodeService.objects.filter(service__in=self.project.services.all()).count() >= settings.FREEMIUM_AVAILABILITY:
            raise ValidationError(f'You can only have {settings.FREEMIUM_AVAILABILITY} service(s)')
        return cleaned_data

     # Override save method to save the project title with the url value
    def save(self, commit=True):

        url = self.cleaned_data['url'].replace('https://', '').replace('http://', '')
        if self.cleaned_data['scheme'] == 'https':
            url = 'https://' + url
        else:
            url = 'http://' + url

        obj = super(HTTPCodeServiceForm, self).save(commit=False)
        obj.url = url
        if not self.cleaned_data['tls_skip_verify']:
            obj.tls_skip_verify = False
        return obj

class MockedHTTPCodeServiceForm(ModelForm):
    class Meta:
        model = HTTPMockedCodeService
        fields = ['code']
