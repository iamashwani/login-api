
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
from decimal import Decimal


class User(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    logo = models.ImageField(upload_to ='profile/', blank=True,null = True)
    profile_id = models.CharField(max_length=200)
    debit_or_credit = models.BooleanField(default=False)
    transaction_amount = models.FloatField(default=0.0)
    curr_available_amount_if_credit_row = models.FloatField(default=0.0)
    transaction_method_record_unique_id = models.CharField(max_length=200)
    transaction_time = models.DateTimeField(default=datetime.datetime.now)
    wallet_debit_record2wallet_credit_record = models.ForeignKey('self', default=None, null=True,  on_delete=models.CASCADE)
    wallet2store_details = models.BigIntegerField(default=0)
    hmac_or_checksum = models.CharField(max_length=200, default='temp_HMAC', blank=True, null=True)
    is_deleted = models.CharField(max_length=45)

    def __str__(self):
        return self.mobile

    def __unicode__(self):
        return str(self.mobile)
