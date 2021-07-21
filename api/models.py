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


class Vector(models.Model):
    id = ApiIdField(prefix="hst")
    product_id = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=512, blank=True)
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
