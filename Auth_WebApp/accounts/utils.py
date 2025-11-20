# accounts/utils.py
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetOTP

def generate_otp(length=6):
    # Alphanumeric characters (uppercase + digits)
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_otp_email(user):
    # 1. Generate Code
    otp_code = generate_otp()

    # 2. Delete any old OTPs for this user (so only the newest one works)
    PasswordResetOTP.objects.filter(user=user).delete()

    # 3. Save new OTP to DB
    PasswordResetOTP.objects.create(user=user, otp_code=otp_code)

    # 4. Send Email
    subject = 'Your Password Reset OTP'
    message = f'Hello {user.username},\n\nYour OTP for password reset is: {otp_code}\n\nThis code expires in 10 minutes.'
    from_email = settings.EMAIL_HOST_USER # or 'webmaster@localhost'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)