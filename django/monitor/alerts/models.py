from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Alert(models.Model):

    user = models.ForeignKey(
        User,
        null=True,
        on_delete = models.CASCADE,
        related_name = "alerts",
        related_query_name = "alert",
    )
    date = models.DateField(auto_now=True, editable=False, help_text="Creation date")
    json = models.TextField(blank=False, help_text="RAW json as received by the webhook")