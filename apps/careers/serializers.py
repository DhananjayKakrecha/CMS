from rest_framework import serializers
from .models import Career

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            "id",
            "title",
            "one_line_desc",
            "freshers_desc",
            "experienced_desc",
            "svg_d_value",
            "updated_at",
        )
        read_only_fields = ("id", "updated_at")

class CareerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            "id",
            "title",
            "one_line_desc",
            "freshers_desc",
            "experienced_desc",
            "svg_d_value",
            "updated_at",
        )

class CareerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            "id",
            "title",
            "one_line_desc",
            "freshers_desc",
            "experienced_desc",
            "svg_d_value",
            "updated_at",
        )
