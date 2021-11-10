# Generated by Django 3.2.7 on 2021-11-10 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='url',
        ),
        migrations.CreateModel(
            name='HTTPMockedCodeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(choices=[(200, '200 - OK'), (404, '404 - Not Found'), (418, '418 - I’m a teapot'), (500, '500 - Internal Server Error')])),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='httpmockedcode', to='projects.service')),
            ],
        ),
        migrations.CreateModel(
            name='HTTPCodeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=512)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='httpcode', to='projects.service')),
            ],
        ),
    ]
