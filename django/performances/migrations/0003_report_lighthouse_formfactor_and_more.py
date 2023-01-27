# Generated by Django 4.1.5 on 2023-01-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0002_performance_last_request_date_alter_performance_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='lighthouse_formFactor',
            field=models.IntegerField(choices=[(0, 'Desktop'), (1, 'Mobile')], default=0, help_text='Lighthouse form factor'),
        ),
        migrations.AddField(
            model_name='report',
            name='lighthouse_score_accessibility',
            field=models.IntegerField(blank=True, help_text='Lighthouse accessibility score', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='lighthouse_score_bestPractices',
            field=models.IntegerField(blank=True, help_text='Lighthouse best practices score', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='lighthouse_score_performance',
            field=models.IntegerField(blank=True, help_text='Lighthouse performance score', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='lighthouse_score_pwa',
            field=models.IntegerField(blank=True, help_text='Lighthouse pwa score', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='lighthouse_score_seo',
            field=models.IntegerField(blank=True, help_text='Lighthouse seo score', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='last_request_date',
            field=models.DateTimeField(blank=True, help_text='Last request date', null=True),
        ),
    ]
