from django.test import TestCase

# Create your tests here.
import base64
import json
from django.test import TestCase
from .views import index
from django.test import Client



# Create your tests here.
class FrontEndTestCase(TestCase):
    def setUp(self):
        pass

    def test_home_badhost(self):
        response = self.client.get('/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_migration_badhost(self):
        response = self.client.get('/migration/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_commands_badhost(self):
        response = self.client.get('/commands/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_changelog_badhost(self):
        response = self.client.get('/changelog/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_privacy_badhost(self):
        response = self.client.get('/privacy/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_tos_badhost(self):
        response = self.client.get('/tos/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_start_badhost(self):
        response = self.client.get('/getting-started/', HTTP_HOST="api.agradehost.com")
        self.assertEqual(response.status_code, 302)

    def test_home(self):
        response = self.client.get('/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)

    def test_migration(self):
        response = self.client.get('/migration/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)

    def test_commands(self):
        response = self.client.get('/commands/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)

    def test_changelog(self):
        response = self.client.get('/changelog/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)

    def test_privacy(self):
        response = self.client.get('/privacy/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)

    def test_tos(self):
        response = self.client.get('/tos/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)

    def test_invite(self):
        response = self.client.get('/invite/')
        self.assertEqual(response.status_code, 302)

    def test_start(self):
        response = self.client.get('/getting-started/', HTTP_HOST="agradehost.com")
        self.assertEqual(response.status_code, 200)
