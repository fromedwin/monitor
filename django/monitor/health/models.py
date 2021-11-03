from django.db import models
from django.contrib.auth.models import User
from applications.models import Service

# Create your models here.
class HealthTest(models.Model):

    HTTP_CODES = [
        (200, '200 - OK'),
        (404, '404 - Not Found'),
        (418, '418 - I’m a teapot'),
        (500, '500 - Internal Server Error'),
    ]

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "healthTest",
        related_query_name = "",
    )
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE,
        related_name = "healthTest",
        related_query_name = "",
        blank=True,
        null=True,
    )
    code = models.IntegerField(choices=HTTP_CODES)
    comment = models.CharField(max_length=256, blank=True, help_text="Max 258 characters")