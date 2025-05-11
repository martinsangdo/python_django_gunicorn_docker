import json
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from io import StringIO
from django.core.management import call_command
import logging
from unittest.mock import patch


class HealthTest(TestCase):
    def test_health_endpoint(self):
        client = Client()
        response = client.get(reverse('health_check'))  # Assuming your URL name is 'health_check'
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, {'status': 'ok', 'database': 'reachable'})


