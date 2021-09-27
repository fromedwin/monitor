import uuid
import ipaddress

from django.db import models
from django.contrib.auth.models import User
from yamlfield.fields import YAMLField
from django.utils import timezone
import math
import datetime
from django.conf import settings

# SEVERITY =(
#     ("CRITICAL", "Critical"),
#     ("WARN", "Warning"),
# )

# class Alerts(models.Model):
#     alert = models.CharField(max_length=200, unique=True, help_text="eg. InstanceDown")
#     expr = models.TextField(help_text="eg. probe_success == 0")
#     waiting_duration = model.CharField(max_length=20, help_text="5m")
#     severity = model.CharField(max_length=8, choices=SEVERITY)
#     summary = model.TextField(help_text="annotation.summary")
#     description = model.TextField(help_text="annotation.description")
#     is_active = model.BooleanField(default=True, help_text="Will be ignored")

class AlertsConfig(models.Model):
    title = models.CharField(max_length=200)
    yaml = YAMLField()

class Server(models.Model):
    ip = models.CharField(max_length=128, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_setup = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "servers",
        blank = True,
        null = True,
    )

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
                return str(seconds) +  "second ago"
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

