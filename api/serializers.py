from rest_framework import serializers

from api import models


class DPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DPU
        fields = "__all__"
        read_only_fields = ("id", "updated_at", "created_date")

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):

        return super().update(instance, validated_data)


class EvSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Events
        exclude = ("space", "door")
