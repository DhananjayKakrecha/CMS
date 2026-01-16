from rest_framework import serializers
from .models import User
from .constants import UserRole

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "password",
            "phone_no",
            "address",
            "role",
            "can_access",
            "is_active",
        )
        read_only_fields = ("id", "role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.role = UserRole.ADMIN
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
    def validate(self, attrs):
        # On CREATE (no instance yet)
        if self.instance is None:
            if not attrs.get("password"):
                raise serializers.ValidationError({
                    "password": "Password is required when creating admin"
                })
        return attrs


class AdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "phone_no",
            "address",
            "can_access",
            "is_active",
            "created_at",
        )
