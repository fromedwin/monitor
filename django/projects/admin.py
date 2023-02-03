from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_favorite')

admin.site.register(Project, ProjectAdmin)
