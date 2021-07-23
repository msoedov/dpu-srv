import arrow
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api import models
from api import serializers


class VectorView(generics.ListCreateAPIView):
    get_serializer = serializers.DPUSerializer
    permission_classes = [AllowAny]
    model = models.DPU


class EventsView(views.APIView):
    permission_classes = [AllowAny]
    queryset = models.Events.objects.all()
    get_serializer = serializers.EvSerializer

    def get(self, request, format=None, **_):
        dt = self.request.query_params.get("dt", "2025-02-26T04:53:58.944Z")
        dt = arrow.get(dt, "YYYY-MM-DDTHH:mm:ss.SSSZ").datetime
        spc = self.kwargs.get("spc")
        record = self.queryset.filter(created_at__lte=dt, space=spc).last()
        record = serializers.EvSerializer(record)
        return Response(record.data, status=200)
