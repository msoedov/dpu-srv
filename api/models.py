import uuid
from enum import Enum

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


class AggregationManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Space(models.Model):
    id = ApiIdField(prefix="spc")
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    details = models.JSONField(default=dict)
    comany = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Doorway(models.Model):
    id = ApiIdField(prefix="drw")
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    spaces = models.ManyToManyField(Space)


class DPU(models.Model):
    id = ApiIdField(prefix="dpu")
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    door = models.ForeignKey(Doorway, on_delete=models.SET_NULL, null=True)


class Events(models.Model):
    id = ApiIdField(prefix="ev")
    door = models.ForeignKey(Doorway, on_delete=models.SET_NULL, null=True)
    direction = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class RealtimeSpaceData(models.Model):
    id = ApiIdField(prefix="rsd")
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    count = models.IntegerField()
