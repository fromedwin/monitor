# Generated by Django 3.2.7 on 2021-11-09 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pager_Duty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routing_key', models.CharField(max_length=32)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pager_duty', to='projects.project')),
            ],
            options={
                'verbose_name': 'Pager Duty key',
                'verbose_name_plural': 'Pager Duty keys',
            },
        ),
    ]
