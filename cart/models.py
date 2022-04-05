from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from decimal import Decimal
import os
import random
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


class User(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    #logo_path = models.CharField(max_length=200)
    logo = models.ImageField(null=True, blank=True)
    profile_id = models.CharField(max_length=200)


class Wallet(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, default=0)
    add_amount = models.DecimalField(_('add amount'), max_digits=10, decimal_places=2, default=0)
    win_amount = models.DecimalField( max_digits=10, decimal_places=2, default=0)
    deduct_amount = models.DecimalField( max_digits=10, decimal_places=2, default=0)