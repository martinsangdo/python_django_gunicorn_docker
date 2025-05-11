import json
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command

from my_app.models.sale import Sale

class HealthTest(TestCase):
    def test_health_endpoint(self):
        client = Client()
        response = client.get(reverse('health_check'))  # Assuming your URL name is 'health_check'
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, {'status': 'ok', 'database': 'reachable'})


class ImportSalesTest(TestCase):
    def test_import_sales(self):
        client = Client()

        response = client.get(reverse('import_sales'))
        self.assertEqual(response.status_code, 201)

        final_row_count = Sale.objects.count()
        #print(final_row_count)
        data = json.loads(response.content)
        self.assertEqual(data, {"imported_rows": final_row_count})


class OverallMetricsTest(TestCase):
    def setUp(self):
        # Seed 5 Sale rows
        Sale.objects.create(date=date(2025, 3, 10), product_id=1, order_id=1, amount_sgd=10.00)
        Sale.objects.create(date=date(2025, 3, 10), product_id=2, order_id=1, amount_sgd=12.00)
        Sale.objects.create(date=date(2025, 3, 11), product_id=3, order_id=2, amount_sgd=15.00)
        Sale.objects.create(date=date(2025, 3, 11), product_id=4, order_id=2, amount_sgd=18.00)
        Sale.objects.create(date=date(2025, 3, 12), product_id=5, order_id=3, amount_sgd=20.00)

    def test_overall_metrics(self):
        client = Client()
        url = reverse('overall_metrics') + '?start=2025-3-10&end=2025-3-12'
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        expected_total = 10.00 + 12.00 + 15.00 + 18.00 + 20.00
        expected_average = expected_total / 3   #3 orders

        self.assertEqual(data['total_revenue_sgd'], expected_total)
        self.assertEqual(data['average_order_value_sgd'], expected_average)

class DailyMetricsTest(TestCase):
    def setUp(self):
        # Seed Sale rows spanning three dates
        Sale.objects.create(date=date(2025, 3, 10), product_id=1, order_id=1, amount_sgd=10.00)
        Sale.objects.create(date=date(2025, 3, 10), product_id=2, order_id=1, amount_sgd=12.00)
        Sale.objects.create(date=date(2025, 3, 11), product_id=3, order_id=2, amount_sgd=15.00)
        Sale.objects.create(date=date(2025, 3, 11), product_id=4, order_id=2, amount_sgd=18.00)
        Sale.objects.create(date=date(2025, 3, 12), product_id=5, order_id=3, amount_sgd=20.00)

    def test_daily_metrics(self):
        client = Client()
        url = reverse('daily_metrics') + '?start=2025-3-10&end=2025-3-12'
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        expected_daily_revenue = [
            {'date':'2025-03-10', 'revenue_sgd': 10.00 + 12.00},
            {'date':'2025-03-11', 'revenue_sgd': 15.00 + 18.00},
            {'date':'2025-03-12', 'revenue_sgd': 20.00}
        ]

        self.assertEqual(len(data), len(expected_daily_revenue))
        for item in expected_daily_revenue:
            self.assertIn(item, data)