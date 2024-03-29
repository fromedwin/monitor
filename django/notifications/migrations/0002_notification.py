# Generated by Django 4.1.5 on 2023-09-05 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('availability', '0001_initial'),
        ('projects', '0001_initial'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('severity', models.IntegerField(choices=[(0, 'unknown'), (1, 'resolved'), (2, 'firing')], default=0)),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='projects.project')),
                ('service', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='availability.service')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
