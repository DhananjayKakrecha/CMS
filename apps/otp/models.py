import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="otps"
    )

    otp_hash = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)

    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_otps"
        ordering = ["-created_at"]

    def set_otp(self, raw_otp: str):
        self.otp_hash = make_password(raw_otp)

    def check_otp(self, raw_otp: str) -> bool:
        return check_password(raw_otp, self.otp_hash)

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at
