from django.forms import ModelForm
from .models import Pager_Duty, Emails

class PagerDutyForm(ModelForm):
	class Meta:
		model = Pager_Duty
		fields = ['routing_key']

class EmailsForm(ModelForm):
    class Meta:
        model = Emails
        fields = ['email']
