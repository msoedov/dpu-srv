import json
import uuid
import tempfile

from django.test import TestCase
from rest_framework.test import APIClient
from mixer.backend.django import mixer

import api.models as models


def jason(**data):
    return dict(content_type="application/json", data=json.dumps(data),)


placeholder = lambda: str(mixer.faker.small_positive_integer())


class VectorApiViewTests(TestCase):
    factory_created = False

    def setUp(self):
        if self.factory_created:
            return
        self.client = APIClient()
        self.api_key = models.Vector.objects.create(email=mixer.faker.email())
        self.auth()
        self.setup_objects()
        self.factory_created = True

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"{self.api_key.id}")

    def setup_objects(self):
        n = 5
        _ = mixer.cycle(n).blend(models.Vector,)
        _ = mixer.cycle(n).blend(models.Vector,)

    def test_key_get_ok(self):
        response = self.client.post(
            "/api/key/promo", **jason(email=mixer.faker.email()),
        )
        self.assertEquals(response.status_code, 200, response.json())
        response = self.client.post(
            "/api/key/lead", **jason(email=mixer.faker.email()),
        )
        self.assertEquals(response.status_code, 200, response.json())

        response = self.client.post(
            "/api/key/test", **jason(email=mixer.faker.email()),
        )
        self.assertEquals(response.status_code, 200, response.json())
        print("json->", response.json())
