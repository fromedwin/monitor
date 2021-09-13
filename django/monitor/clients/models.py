from django.db import models
from yamlfield.fields import YAMLField

class AlertsConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()

class PrometheusConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()

class Server(models.Model):
    uuid = models.CharField(max_length=128, blank=False, unique=True)
    ip = models.CharField(max_length=128, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()
