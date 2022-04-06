
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from decimal import Decimal
from .errors import InsufficientBalance
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db import transaction

class User(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    #logo_path = models.CharField(max_length=200)
    logo = models.ImageField(null=True, blank=True)
    profile_id = models.CharField(max_length=200)

class Wallet(models.Model):
    user = models.ForeignKey(User,null=True,related_name='wallet_mobile',on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('Total amount'), max_digits=10, decimal_places=2, default=10)
    add_amount = models.DecimalField(_('Add amount'), max_digits=10, decimal_places=2, default=0)
    win_amount = models.DecimalField( max_digits=10, decimal_places=2, default=0)
    deduct_amount = models.DecimalField( max_digits=10, decimal_places=2, default=0)
    

    # @transaction.atomic
    # def deposit(self, amount):
    #     """ Deposit `amount` to wallet.
    #     """

    #     amount = Decimal(amount)
    #     self.transaction_set.create(
    #         amount=amount,
    #         running_balance=self.total_amount + amount
    #     )
    #     self.total_amount += amount
    #     self.save()