from django.forms import ModelForm, URLField, CharField
from .models import Performance

class PerformanceForm(ModelForm):

    url = URLField(help_text="URL must start with http:// or https://")
    scheme = CharField(max_length=5, help_text="URL must start with http:// or https://")

    class Meta:
        model = Performance
        fields = ['scheme', 'url']

    # On init we set scheme value with http if url start with https or http if url start with url
    def __init__(self, *args, **kwargs):
        super(PerformanceForm, self).__init__(*args, **kwargs)
        if self.instance.url:
            if self.instance.url.startswith('https://'):
                self.initial['scheme'] = 'https'
                self.initial['url'] = self.instance.url.replace('https://', '')
            else:
                self.initial['scheme'] = 'http'
                self.initial['url'] = self.instance.url.replace('http://', '')

     # Override save method to save the project title with the url value
    def save(self, commit=True):

        url = self.cleaned_data['url'].replace('https://', '').replace('http://', '')
        if self.cleaned_data['scheme'] == 'https':
            url = 'https://' + url
        else:
            url = 'http://' + url

        obj = super(PerformanceForm, self).save(commit=False)
        obj.url = url
        return obj
