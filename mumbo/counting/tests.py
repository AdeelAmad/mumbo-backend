from django.test import TestCase
from .models import Count
from .views import index
from django.test.client import RequestFactory

import sys
sys.path.append('../mumbo')

from management.models import Guild


# Create your tests here.
class CountTestCase(TestCase):
    def setUp(self):
        guild = Guild.objects.create(id="12345678901234567890")
        self.c = Count.objects.create(guild_id=guild)
        self.factory = RequestFactory()

    def test_get_count_no_auth(self):
        request = self.factory.get('/counting/')
        value = index(request)
        self.assertEqual(value.status_code, 302)