from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from decimal import Decimal
import os
import random
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from django.core.validators import RegexValidator


class User(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    profile = models.ImageField(null=True, blank=True)
    profile_url = models.CharField(max_length=200)
    profile_id = models.IntegerField(default=0)




class Wallet(models.Model):
    user = models.ForeignKey(User,null=True,related_name='wallet_mobile',on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.FloatField(_('Total amount'), default=10)
    add_amount = models.FloatField(_('Add amount'), default=0)
    total_add_amount = models.FloatField(_('Total Add amount') , default=0)
    win_amount = models.FloatField( default=0)
    total_win_amount = models.FloatField( default=0)
    deduct_amount = models.FloatField(default=0)
