# Generated by Django 3.2.7 on 2021-09-27 16:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20210922_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='last_modified_setup',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]