# Generated by Django 3.2.7 on 2021-10-06 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0004_auto_20211006_0849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instancedownalert',
            options={'verbose_name': 'Service down alert', 'verbose_name_plural': 'Service down alerts'},
        ),
        migrations.AddField(
            model_name='genericalert',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='genericalert',
            name='endsAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genericalert',
            name='instance',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='genericalert',
            name='severity',
            field=models.IntegerField(choices=[(0, 'unknown'), (1, 'warning'), (2, 'critical')], default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genericalert',
            name='startsAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 6, 12, 23, 48, 949380)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genericalert',
            name='status',
            field=models.IntegerField(choices=[(0, 'unknown'), (1, 'resolved'), (2, 'firing')], default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genericalert',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
