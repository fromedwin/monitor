import uuid
import ipaddress
import math
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from yamlfield.fields import YAMLField

from incidents.models import INCIDENT_SEVERITY

class Alerts(models.Model):
    alert = models.CharField(max_length=128)
    expr = models.CharField(max_length=128)
    duration = models.CharField(max_length=8)
    severity = models.IntegerField(choices=INCIDENT_SEVERITY)
    summary = models.TextField()
    description = models.TextField()

class Server(models.Model):
    ip = models.CharField(max_length=128, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_setup = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)

    # URL used to fetch server
    url = models.CharField(max_length=256, blank=False, default='host.docker.internal')
    port = models.IntegerField(blank=False, default=8001)

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "servers",
        blank = True,
        null = True,
    )

    @property
    def protocol(self):
        return 'https' if self.url != 'host.docker.internal' else 'http'

    @property
    def is_active(self):
        return self.last_seen > (timezone.now() - datetime.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5))

    @property
    def is_public(self):
        if self.ip =='localhost':
            return False
        return not ipaddress.IPv4Address(self.ip).is_private

    @property
    def last_seen_from(self):
        now = timezone.now()
        diff= now - self.last_seen

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"
        return self.last_seen

class AuthBasic(models.Model):
    """
    Server can be protected with Basic Authentication.
    Credentials are generated and provided by the server on registration.
    """
    server = models.ForeignKey(
        Server,
        on_delete = models.CASCADE,
        related_name = "authbasic"
    )
    username = models.CharField(max_length=128, blank=False)
    password = models.CharField(max_length=128, blank=False)

class Metrics(models.Model):
    """
    Fetch {{url}}/metrics within prometheus
    Can be used for node_explorer or custom metrics
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "metrics",
    )
    url = models.URLField(max_length=512, blank=False)
    is_enabled = models.BooleanField(default=True)
