# Generated by Django 4.1.5 on 2023-09-05 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('availability', '0001_initial'),
        ('notifications', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='availability.service'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='severity',
            field=models.IntegerField(choices=[(0, 'unknown'), (1, 'warning'), (2, 'critical'), (3, 'resolved')], default=0),
        ),
    ]
