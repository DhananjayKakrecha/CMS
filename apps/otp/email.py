from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Your Login OTP"
    message = f"""
Hello,

Your One-Time Password (OTP) is:

{otp}

This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.

If you did not request this, please ignore this email.

Thanks,
CMS Security Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
