# Generated by Django 3.2.7 on 2022-01-07 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_delete_alertsconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthBasic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authbasic', to='clients.server')),
            ],
        ),
    ]