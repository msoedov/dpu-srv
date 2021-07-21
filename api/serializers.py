import time
from functools import lru_cache

from api import models
from django.conf import settings
from rest_framework import serializers


class VectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vector
        fields = "__all__"
        read_only_fields = ("id", "updated_at", "created_date")

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
