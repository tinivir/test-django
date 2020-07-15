from rest_framework import serializers
from wt.usage.models import UsageRecord


class UsageSerializer(serializers.ModelSerializer):
    price_limit_exceed = serializers.SerializerMethodField(method_name='calulate_price_difference')

    class Meta:
        model = UsageRecord
        fields = (
            'att_subscription_id',
            'sprint_subscription_id',
            'usage_type',
            'price_limit_exceed',
        )

    def calulate_price_difference(self, obj):
        price_limit = int(self.context['request'].query_params.get('price_limit', 0))
        return obj.price - price_limit


class AggregatedUsageSerializer(serializers.ModelSerializer):
    date=serializers.DateTimeField()
    total_price=serializers.IntegerField()
    total_usage=serializers.IntegerField()

    class Meta:
        model = UsageRecord
        fields = (
            'att_subscription_id', 
            'sprint_subscription_id', 
            'date', 
            'total_price', 
            'total_usage'
        )