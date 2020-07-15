from unittest import mock

from django.test import TestCase
from model_mommy import mommy

from wt.usage.serializers import UsageSerializer


class UsageSerializerTest(TestCase):

    @mock.patch('wt.usage.serializers.UsageSerializer.calulate_price_difference')
    def test_serializer(self, mocked_price_difference) :
        usage = mommy.make('usage.UsageRecord', price = 2)
        mocked_price_difference.return_value = 1

        data = UsageSerializer(usage).data

        self.assertEqual(data['att_subscription_id'], usage.att_subscription_id)
        self.assertEqual(data['sprint_subscription_id'], usage.sprint_subscription_id)
        self.assertEqual(data['usage_type'], usage.usage_type)
        self.assertEqual(data['price_limit_exceed'], 1)