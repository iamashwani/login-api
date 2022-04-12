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
    phone_regex = RegexValidator(regex=r'^\+?1?\d{6,15}$',
                                 message="Mobile incorrect.")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    # mobile = models.IntegerField(max_length=17, blank=True,null=True)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200,null=True, blank=True,)
    username = models.CharField(max_length=200,null=True, blank=True,)
    profile = models.ImageField(null=True, blank=True)
    profile_url = models.CharField(max_length=200)
    profile_id = models.IntegerField(default=0)


class Wallet(models.Model):
    user = models.ForeignKey(User, null=True, related_name='wallet_mobile', on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('Total amount'), max_digits=10, decimal_places=2, default=10)
    add_amount = models.DecimalField(_('Add amount'), max_digits=10, decimal_places=2, default=0)
    deposit_cash = models.DecimalField(_('Full Add amount'), max_digits=10, decimal_places=2, default=0)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    winning_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdraw_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

