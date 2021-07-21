import os
import time
import hashlib
import datetime
from functools import lru_cache

from django.http import HttpResponseRedirect
from rest_framework import views
from rest_framework import generics
from rest_framework import serializers
from django.core.files.base import ContentFile
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer

from api import models
from api import serializers


class VectorView(generics.ListCreateAPIView):
    get_serializer = serializers.VectorSerializer
    permission_classes = [AllowAny]
    model = models.Vector


class ReadVectorView(generics.RetrieveUpdateDestroyAPIView):
    get_serializer = serializers.VectorSerializer
    permission_classes = [AllowAny]
    model = models.Vector

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
