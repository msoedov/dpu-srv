import uuid
from enum import Enum
from functools import lru_cache
from django.db import models
from django.db.utils import IntegrityError

Srv = Enum("Srv", "one two three")

IntegrityError = IntegrityError


class ApiIdField(models.CharField):
    """
    Inspired by Stripe api ids format which super intuitive in documentation and examples

    >>> class Custom(models.Model):
            id = ApiIdField(prefix="cst")
    'cst_128185cb11134e2c95263847b31f09'
    """

    def __init__(self, **opts):
        self.prefix = opts.pop("prefix", None)
        opts["primary_key"] = True
        opts["editable"] = False
        opts["max_length"] = opts.pop("max_length", 34)
        super().__init__(**opts)

    def get_default(self):
        key = uuid.uuid4().hex
        return f"{self.prefix}_{key}"[: self.max_length]


class CustomManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @lru_cache(256)
    def motion_direction(self, dpu: str or "DPU", direction=1) -> ("Space", "Space"):
        if isinstance(dpu, str):
            dpu = DPU.objects.get(id=dpu)
        if not dpu:
            return None
        if direction == 1:
            return dpu.door.ingress_spc, dpu.door.egress_spc
        return dpu.door.egress_spc, dpu.door.ingress_spc


class Space(models.Model):
    id = ApiIdField(prefix="spc")
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    meta_details = models.JSONField(default=dict)
    company = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Doorway(models.Model):
    id = ApiIdField(prefix="drw")
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    meta_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    egress_spc = models.ForeignKey(
        Space, on_delete=models.CASCADE, related_name="egress"
    )
    ingress_spc = models.ForeignKey(
        Space, on_delete=models.CASCADE, related_name="ingress"
    )


class DPU(models.Model):
    id = ApiIdField(prefix="dpu")
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    meta_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    door = models.ForeignKey(Doorway, on_delete=models.SET_NULL, null=True)

    objects = CustomManager()


class Events(models.Model):
    id = ApiIdField(prefix="ev")
    door = models.ForeignKey(Doorway, on_delete=models.SET_NULL, null=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="events")
    direction = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    new_count = models.IntegerField(default=0)


class RealtimeSpaceData(models.Model):
    id = ApiIdField(prefix="rsd")
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
