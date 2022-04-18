from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from decimal import Decimal
import os
import random
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
from cart.storage import OverwriteStorage


def content_file_name(instance, filename):
    extension = filename.split(".")[-1]
    ext2 = filename.replace(extension, "png")
    og_filename = ext2.split('.')[0]
    og_filename2 = ext2.replace(og_filename, str(instance.id))
    return os.path.join('', og_filename2)


class User(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile incorrect.")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    # mobile = models.IntegerField(max_length=17, blank=True,null=True)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200,null=True, blank=True,)
    username = models.CharField(max_length=200,null=True, blank=True,)
    profile = models.ImageField(upload_to=content_file_name, storage=OverwriteStorage(), blank=True)
    profile_url = models.CharField(max_length=200)
    profile_id = models.IntegerField(default=0)
    referral = models.CharField(max_length=150)


class Wallet(models.Model):
    user = models.ForeignKey(User, null=True, related_name='wallet_mobile', on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.FloatField(_('Total amount'), default=10)
    add_amount = models.FloatField(_('Add amount'), default=0)
    deposit_cash = models.FloatField(_('Full Add amount'),default=0)
    win_amount = models.FloatField(default=0)
    winning_cash = models.FloatField(default=0)
    withdraw_amount = models.FloatField(default=0)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2, default=10)
    description = models.CharField(max_length=200, null=True, blank=True, )


class Transcations(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=200,blank=True,)
    winning_cash = models.FloatField(default=0)
    insert_date_and_time = models.DateTimeField(null=True, auto_now_add=True)


# class ReferralRelationship(models.Model):
#     # who invite
#     employer = models.ForeignKey(User,related_name='inviter',verbose_name="inviter",on_delete=models.CASCADE,)
#     # who connected
#     employee = models.ForeignKey(User,related_name='invited',verbose_name="invited",on_delete=models.CASCADE,)
#     # referral code
#     refer_token = models.ForeignKey("ReferralCode",related_name="referral_code",verbose_name="referral_code",on_delete=models.CASCADE,)
#
# class ReferralCode(models.Model):
#     token = models.CharField(unique=True, max_length=150)
#     user = models.ForeignKey(User, verbose_name="code_master", on_delete=models.CASCADE)




