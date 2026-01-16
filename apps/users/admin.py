from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "role",
        "can_access",
        "is_active",
        "created_at",
    )

    list_filter = ("role", "can_access", "is_active")
    search_fields = ("email", "full_name", "phone_no")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Info", {
            "fields": ("full_name", "email", "phone_no", "address")
        }),
        ("Security", {
            "fields": ("password",)
        }),
        ("Permissions", {
            "fields": ("role", "can_access", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )
