from datetime import datetime, timedelta
from unittest import mock

from django.test import TestCase
from model_mommy import mommy

from wt.usage.models import AggreatedUsageRecordManager, UsageRecord


class UsageRecordTest(TestCase):

    def test_manager(self):
        data_usage = mommy.make('usage.UsageRecord', _quantity=3, 
            usage_type='data', usage_date=datetime.now(), data_used=3, price=5)
        data_usage_day_before = mommy.make('usage.UsageRecord', _quantity=4, 
            usage_type='data', usage_date=datetime.now()-timedelta(days=1), data_used=3, price=5)
        voice_usage = mommy.make('usage.UsageRecord', _quantity=3, 
            usage_type='voice', usage_date=datetime.now(), data_used=3, price=5)
        voice_usage_day_before = mommy.make('usage.UsageRecord', _quantity=4, 
            usage_type='voice', usage_date=datetime.now()-timedelta(days=1), data_used=3, price=5)
        
        self.assertEqual(len(UsageRecord.aggregated_objects.all()), 2)
        list_obj = list(UsageRecord.aggregated_objects.all())
        self.assertEqual(list_obj[0]['total_price'], 40.00)
        self.assertEqual(list_obj[0]['total_usage'], 24)
        self.assertEqual(list_obj[1]['total_price'], 30.00)
        self.assertEqual(list_obj[1]['total_usage'], 18)