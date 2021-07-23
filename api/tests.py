import json

from django.test import TestCase
from rest_framework.test import APIClient
from mixer.backend.django import mixer

import api.models as models


def jason(**data):
    return dict(content_type="application/json", data=json.dumps(data),)


placeholder = lambda: str(mixer.faker.small_positive_integer())


class EventApiViewTests(TestCase):
    factory_created = False

    def setUp(self):
        if self.factory_created:
            return
        self.client = APIClient()
        self.api_key = "xx"
        self.auth()
        self.setup_objects()
        self.factory_created = True

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"{'self.api_key.id}'}")

    def setup_objects(self):
        n = 5
        _ = mixer.cycle(n).blend(models.Events,)
        _ = mixer.cycle(n).blend(models.Events,)

    def test_key_get_ok(self):
        response = self.client.get("/api/events/spc_65b67b69acac4b6d80ffffb1a99d8f",)
        self.assertEquals(response.status_code, 200, response.json())
