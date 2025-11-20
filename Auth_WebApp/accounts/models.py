from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    # Add more custom fields here if you want

    def __str__(self):
        return self.email
    
class PasswordResetOTP(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # valid for 10 minutes
        return self.created_at >= timezone.now() - datetime.timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.email}"