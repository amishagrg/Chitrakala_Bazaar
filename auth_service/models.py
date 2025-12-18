from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

# Custom User model
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    # We can add more fields here if needed

    def __str__(self):
        return self.username

# OTP model
class OTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - OTP"

