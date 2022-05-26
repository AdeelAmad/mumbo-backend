import base64
import json

from django.test import TestCase
from django.test import Client

import sys
sys.path.append('../mumbo')

from management.models import Guild


# Create your tests here.
class VCTestCase(TestCase):
    def setUp(self):
        g = Guild.objects.create(id="123456789012345678")
        Guild.objects.create(id="734506404093624470")
        g.voicechannelsetting_set.create()
        g.save()
        self.client = Client()
        self.username = "bot"
        self.password = "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ"

    def test_get_vc_no_auth(self):
        response = self.client.get('/voicechannels/')
        self.assertEqual(response.status_code, 302)

    def test_get_vc_incorrect_auth(self):
        credentials = f"{self.username}:eeeeeeeeee"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/voicechannels/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 302)

    def test_bad_method_vc_correct_auth(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/voicechannels/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 405)

    def test_get_vc_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.get('/voicechannels/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_get_vc_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/voicechannels/', json.dumps({"id": 123456789012345679}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_get_vc_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/voicechannels/', json.dumps({"id": 123456789012345678}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)


    def test_put_vc_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 111111111111111111
        }
        response = self.client.put('/voicechannels/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_put_vc_correct_auth_goodid_missing_data(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678
        }
        response = self.client.put('/voicechannels/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_put_count_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678,
            "channel_id": 1,
            "category": 1,
            "bitrate": 1
        }
        response = self.client.put('/voicechannels/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)




    def test_post_vc_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 734506404093624470
        }
        response = self.client.post('/voicechannels/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)

    def test_post_count_correct_auth_dupeid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678
        }
        response = self.client.post('/voicechannels/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 409)

    def test_post_count_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
        }
        response = self.client.post('/voicechannels/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

class ChannelTestCase(TestCase):
    def setUp(self):
        g = Guild.objects.create(id="123456789012345678")
        g.voicechannelsetting_set.create()
        g.save()
        self.client = Client()

        self.username = "bot"
        self.password = "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ"

        self.credentials = f"{self.username}:{self.password}"
        self.base64_credentials = base64.b64encode(self.credentials.encode('utf8')).decode('utf8')

    def test_get_channel_no_auth(self):
        response = self.client.get('/voicechannels/channel/')
        self.assertEqual(response.status_code, 302)

    def test_get_channel_incorrect_auth(self):
        credentials = f"{self.username}:eeeeeeeeee"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/voicechannels/channel/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 302)

    def test_bad_method_channel_correct_auth(self):
        response = self.client.patch('/voicechannels/channel/', HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 405)

    def test_get_channel_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.get('/voicechannels/channel/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_get_channel_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/voicechannels/channel/', json.dumps({"id": 123456789012345679}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_get_channel_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/voicechannels/', json.dumps({"id": 123456789012345678}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)
