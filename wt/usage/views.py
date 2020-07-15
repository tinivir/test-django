from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from django_filters import rest_framework as filters

from wt.usage.models import UsageRecord
from wt.usage.serializers import UsageSerializer, AggregatedUsageSerializer


class UsageFilter(filters.FilterSet):
    price_limit = filters.NumberFilter(field_name="price", lookup_expr='gte')
    date = filters.DateFromToRangeFilter()
    usage_type = filters.ChoiceFilter(choices=UsageRecord.TYPE)

    class Meta:
        model = UsageRecord
        fields = ['price_limit', 'usage_type', 'date']


class SubscriptionsView(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = UsageRecord.objects.all()
    serializer_class = UsageSerializer
    filterset_class = UsageFilter

    def get_serializer_class(self):
        if self.request.query_params.get('usage_type'):
            return AggregatedUsageSerializer
        return UsageSerializer
            
    def get_queryset(self):
        if self.request.query_params.get('usage_type'):
            return UsageRecord.aggregated_objects.all()
        return super().get_queryset()
