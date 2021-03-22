from django.contrib import admin
from .models import HealthTest

class HealthTestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'code', 'comment')

admin.site.register(HealthTest, HealthTestAdmin)
