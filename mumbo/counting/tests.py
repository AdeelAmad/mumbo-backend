import base64
import json

from django.test import TestCase
from .models import Count
from .views import index
from django.test import Client

import sys
sys.path.append('../mumbo')

from management.models import Guild


# Create your tests here.
class CountTestCase(TestCase):
    def setUp(self):
        guild = Guild.objects.create(id="123456789012345678")
        Guild.objects.create(id="734506404093624470")
        self.c = Count.objects.create(guild_id=guild)
        self.client = Client()
        self.username = "bot"
        self.password = "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ"

    def test_get_count_no_auth(self):
        response = self.client.get('/counting/')
        self.assertEqual(response.status_code, 302)

    def test_get_count_incorrect_auth(self):
        credentials = f"{self.username}:eeeeeeeeee"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/counting/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 302)

    def test_bad_method_count_correct_auth(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/counting/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 405)

    def test_get_count_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.get('/counting/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_get_count_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/counting/', json.dumps({"id": 123456789012345679}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_get_count_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/counting/', json.dumps({"id": 123456789012345678}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)

    def test_put_count_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 111111111111111111
        }
        response = self.client.put('/counting/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_put_count_correct_auth_goodid_missing_data(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678
        }
        response = self.client.put('/counting/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_put_count_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678,
            "channel": 783017551809740821,
            "last_count": 1000,
            "last_counter": 534932557209403412
        }
        response = self.client.put('/counting/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)




    def test_post_count_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 734506404093624470
        }
        response = self.client.post('/counting/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)

    def test_post_count_correct_auth_dupeid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678
        }
        response = self.client.post('/counting/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 409)

    def test_post_count_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
        }
        response = self.client.post('/counting/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)