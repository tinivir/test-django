from django.db import models
from django.db.models.functions import TruncDay
from model_utils import Choices

from wt.att_subscriptions.models import ATTSubscription
from wt.sprint_subscriptions.models import SprintSubscription

class AggreatedUsageRecordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(date=models.functions.TruncDay('usage_date'))\
                .values('date')\
                .annotate(total_price=models.Sum('price'), total_usage=models.Sum('data_used'))\
                .values('att_subscription_id', 'sprint_subscription_id', 'date', 'total_price', 'total_usage')  


class UsageRecord(models.Model):
    TYPE = Choices(
        ('data', 'Data'),
        ('voice', 'Voice'),
    )
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=True)
    data_used = models.IntegerField(null=False)
    usage_type = models.CharField(max_length=10, choices=TYPE)
    
    objects = models.Manager()
    aggregated_objects = AggreatedUsageRecordManager()
