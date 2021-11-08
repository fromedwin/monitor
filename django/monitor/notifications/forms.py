from django.forms import ModelForm
from .models import Pager_Duty

class PagerDutyForm(ModelForm):
	class Meta:
		model = Pager_Duty
		fields = ['routing_key']