# Generated by Django 4.1.5 on 2023-03-23 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('availability', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='httpcodeservice',
            name='tls_skip_verify',
            field=models.BooleanField(default=False, help_text='Skip TLS certificate verification'),
        ),
    ]
