import json
from datetime import datetime
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder

from api import models

from django.contrib import admin


class ChartJsMixin:
    change_list_template = "dash.html"

    def changelist_view(self, request, extra_context=None):
        last_month = datetime.today() - timedelta(days=30)
        # Aggregate new subscribers per day
        chart_data = (
            self.model.objects.filter(created_at__gte=last_month)
            .annotate(d=TruncDay("created_at"))
            .values("d")
            .annotate(y=Count("id"))
            .order_by("-d")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(models.Vector)
class VectorAdmin(ChartJsMixin, admin.ModelAdmin):
    search_fields = ("id",)
    list_display = (
        "id",
        "created_at",
    )
