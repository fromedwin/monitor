# Generated by Django 4.2.13 on 2024-10-10 13:01

from django.db import migrations, models
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='favicon',
            field=models.ImageField(blank=True, help_text="Application's favicon", null=True, upload_to=projects.models.project_favicon_path),
        ),
    ]
