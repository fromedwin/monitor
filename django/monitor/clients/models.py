import uuid
from django.db import models
from yamlfield.fields import YAMLField

class AlertsConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()

class PrometheusConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()

class Server(models.Model):
    ip = models.CharField(max_length=128, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_seen = models.DateTimeField(auto_now_add=True)


