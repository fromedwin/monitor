from django.contrib import admin
from .models import Emails

class EmailsAdmin(admin.ModelAdmin):
    list_display = ('project', 'email')

admin.site.register(Emails, EmailsAdmin)
