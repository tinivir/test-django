from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from model_utils import Choices, models as models_utils

from wt.plans.models import Plan


class ATTSubscription(models_utils.TimeStampedModel):
    ONE_KILOBYTE_PRICE = Decimal('0.001')
    ONE_SECOND_PRICE = Decimal('0.001')

    """Represents a subscription with AT&T for a user and a single device"""
    STATUS = Choices(
        ('new', 'New'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT) # Owning user

    plan = models.ForeignKey(Plan, null=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS.new)

    device_id = models.CharField(max_length=20, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    phone_model = models.CharField(max_length=128, blank=True, default='')
    network_type = models.CharField(max_length=5, blank=True, default='')

    effective_date = models.DateTimeField(null=True)

    deleted = models.BooleanField(default=False)
