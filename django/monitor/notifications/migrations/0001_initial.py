# Generated by Django 3.2.7 on 2021-10-06 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0004_delete_notify_pager_duty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pager_Duty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routing_key', models.CharField(max_length=32)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pager_duty', to='applications.application')),
            ],
        ),
    ]
