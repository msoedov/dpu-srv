
from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from api import models
from api import serializers


class VectorView(generics.ListCreateAPIView):
    get_serializer = serializers.DPUSerializer
    permission_classes = [AllowAny]
    model = models.DPU


class ReadVectorView(generics.RetrieveUpdateDestroyAPIView):
    get_serializer = serializers.DPUSerializer
    permission_classes = [AllowAny]
    model = models.DPU

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
