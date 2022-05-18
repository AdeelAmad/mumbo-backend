import base64
import json

from django.test import TestCase
from django.test import Client
from .models import Guild
from .views import get_cursor, init_db


# Create your tests here.
class GuildTestCase(TestCase):
    def setUp(self):
        guild = Guild.objects.create(id="123456789012345678")
        Guild.objects.create(id="734506404093624470")
        self.client = Client()
        self.username = "bot"
        self.password = "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ"

    def test_cursor(self):
        conn = init_db()
        cur = get_cursor(conn)
        self.assertIsNotNone(cur)

    def test_cursor_error(self):
        cur = get_cursor(conn=None)
        self.assertIsNotNone(cur)

    def test_get_guild_no_auth(self):
        response = self.client.get('/management/')
        self.assertEqual(response.status_code, 302)

    def test_get_guild_incorrect_auth(self):
        credentials = f"{self.username}:eeeeeeeeee"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/management/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 302)

    def test_bad_method_guild_correct_auth(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/management/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 405)

    def test_get_guild_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/management/', json.dumps({"id": 123456789012345678}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)

    def test_get_guild_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('GET', '/management/', json.dumps({"id": 123456789012345679}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_get_guild_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.get('/management/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_post_guild_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('POST', '/management/', json.dumps({"id": 123456789012345679}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)

    def test_post_guild_correct_auth_dupeid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.generic('POST', '/management/', json.dumps({"id": 123456789012345678}), HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 409)

    def test_post_guild_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.post('/management/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_put_guild_correct_auth_noid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.put('/management/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_put_guild_correct_auth_badid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 111111111111111111
        }
        response = self.client.put('/management/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_put_guild_correct_auth_goodid_missing_data(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678
        }
        response = self.client.put('/management/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_put_guild_correct_auth_goodid(self):
        credentials = f"{self.username}:{self.password}"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        data = {
            "id": 123456789012345678,
            "counting": True,
            "voicechannel": True,
            "leveling": True,
            "afkmusic": True,
            "alert": True
        }
        response = self.client.put('/management/', json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 200)

class MigrateTestCase(TestCase):
    def setUp(self):
        Guild.objects.create(id="123456789012345678", migrated=True)
        guild = Guild.objects.create(id="734506404093624470")
        guild.count_set.create()
        guild.voicechannelsetting_set.create()
        guild.levelingsetting_set.create()
        guild2 = Guild.objects.create(id="123456789012345677")
        guild2.count_set.create()
        guild2.voicechannelsetting_set.create()
        guild2.levelingsetting_set.create()

        self.client = Client()
        self.username = "bot"
        self.password = "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ"

        self.credentials = f"{self.username}:{self.password}"
        self.base64_credentials = base64.b64encode(self.credentials.encode('utf8')).decode('utf8')



    def test_get_migrate_no_auth(self):
        response = self.client.get('/management/migrate/')
        self.assertEqual(response.status_code, 302)

    def test_get_migrate_incorrect_auth(self):
        credentials = f"{self.username}:eeeeeeeeee"
        base64_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        response = self.client.patch('/management/migrate/', HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        self.assertEqual(response.status_code, 302)

    def test_bad_method_migrate_correct_auth(self):
        response = self.client.patch('/management/migrate/', HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 405)

    def test_get_migrate_correct_auth_noid(self):
        response = self.client.get('/management/migrate/', HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_get_migrate_correct_auth_badid(self):
        response = self.client.generic('GET', '/management/migrate/', json.dumps({"id": 123456789012345679}), HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 400)

    def test_get_migrate_correct_auth_goodid_migrated(self):
        response = self.client.generic('GET', '/management/migrate/', json.dumps({"id": 123456789012345678}), HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 404)

    def test_get_migrate_correct_auth_goodid_no_old_data(self):

        response = self.client.generic('GET', '/management/migrate/', json.dumps({"id": 123456789012345677}), HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 406)

    def test_get_migrate_correct_auth_goodid(self):
        response = self.client.generic('GET', '/management/migrate/', json.dumps({"id": 734506404093624470}), HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}")
        self.assertEqual(response.status_code, 200)

