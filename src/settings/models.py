from django.db import models
from django.contrib.auth.models import User
from timezone_field import TimeZoneField

# Define a user profile related to django user model with a timezone field
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    disable_auto_redirect = models.BooleanField(default=False, help_text="Disable auto-redirect from homepage to dashboard")
    timezone = TimeZoneField(null=True, choices_display="STANDARD")

    def directory_path(self):
        return f'user_{self.user.pk}'
