import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from .constants import UserRole

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    phone_no = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)

    role = models.CharField(
        max_length=20,
        choices=UserRole.CHOICES,
        default=UserRole.ADMIN,
    )

    can_access = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.role})"
    
    def set_password(self, raw_password: str):
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)
    
    def is_super_admin(self):
        return self.role == UserRole.SUPER_ADMIN

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def has_cms_access(self):
        if self.is_super_admin():
            return True
        return self.can_access


