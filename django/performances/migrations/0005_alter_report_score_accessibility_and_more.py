# Generated by Django 4.1.5 on 2023-01-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0004_rename_lighthouse_formfactor_report_form_factor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='score_accessibility',
            field=models.FloatField(blank=True, help_text='Lighthouse accessibility score', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='score_best_practices',
            field=models.FloatField(blank=True, help_text='Lighthouse best practices score', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='score_performance',
            field=models.FloatField(blank=True, help_text='Lighthouse performance score', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='score_pwa',
            field=models.FloatField(blank=True, help_text='Lighthouse pwa score', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='score_seo',
            field=models.FloatField(blank=True, help_text='Lighthouse seo score', null=True),
        ),
    ]