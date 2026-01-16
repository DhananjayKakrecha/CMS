from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .email import send_otp_email
from .models import OTP
from .utils import generate_otp

def create_and_send_otp(user):
    """
    - Invalidates previous OTPs
    - Generates new OTP
    - Saves hashed OTP
    - Sends email
    """

    # Invalidate previous OTPs
    OTP.objects.filter(user=user, is_used=False).update(is_used=True)

    raw_otp = generate_otp()

    expiry_minutes = int(settings.OTP_EXPIRY_MINUTES)
    expires_at = timezone.now() + timedelta(minutes=expiry_minutes)

    otp_obj = OTP.objects.create(
        user=user,
        expires_at=expires_at,
    )
    otp_obj.set_otp(raw_otp)
    otp_obj.save()

    send_otp_email(user.email, raw_otp)

    return True

def verify_otp(user, raw_otp: str) -> bool:
    try:
        otp_obj = OTP.objects.filter(
            user=user,
            is_used=False
        ).latest("created_at")
    except OTP.DoesNotExist:
        return False

    if otp_obj.is_expired():
        return False

    if not otp_obj.check_otp(raw_otp):
        return False

    otp_obj.is_used = True
    otp_obj.save(update_fields=["is_used"])

    return True
