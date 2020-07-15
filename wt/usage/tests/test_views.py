from datetime import datetime, timedelta
from rest_framework.test import APIRequestFactory

from django.urls import reverse_lazy
from django.test import TestCase
from model_mommy import mommy

from wt.usage.views import SubscriptionsView


class SubscriptionsTest(TestCase):

    def test_price_limit(self):
        data_usage = mommy.make('usage.UsageRecord', usage_type='data', usage_date=datetime.now(), data_used=3, price=5)
        voice_usage = mommy.make('usage.UsageRecord', usage_type='voice', usage_date=datetime.now(), data_used=3, price=6)

        response = self.client.get(reverse_lazy('api:usage-list')+'?price_limit=4')
        self.assertContains(response, '"price_limit_exceed":1.0')
        self.assertContains(response, '"price_limit_exceed":2.0')

    def test_aggregation(self):
        data_usage = mommy.make('usage.UsageRecord', _quantity=3, 
            usage_type='data', usage_date=datetime.now(), data_used=3, price=5)
        data_usage_day_before = mommy.make('usage.UsageRecord', _quantity=4, 
            usage_type='data', usage_date=datetime.now()-timedelta(days=1), data_used=3, price=5)
        voice_usage = mommy.make('usage.UsageRecord', _quantity=3, 
            usage_type='voice', usage_date=datetime.now(), data_used=3, price=5)
        voice_usage_day_before = mommy.make('usage.UsageRecord', _quantity=4, 
            usage_type='voice', usage_date=datetime.now()-timedelta(days=1), data_used=3, price=5)

        response = self.client.get(reverse_lazy('api:usage-list')+'?usage_type=voice')
        self.assertContains(response, '"total_price":20')
        self.assertContains(response, '"total_usage":12')