from django.db import models
from yamlfield.fields import YAMLField

class AlertsConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()

class PrometheusConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()
