from __future__ import unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
from cart.storage import OverwriteStorage


def content_file_name(instance, filename):
    extension = filename.split(".")[-1]
    ext2 = filename.replace(extension, "png")
    og_filename = ext2.split('.')[0]
    og_filename2 = ext2.replace(og_filename, str(instance.id))
    return os.path.join('profile/', og_filename2)


class User(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    logo = models.ImageField(upload_to = "" ,null=True, blank=True)
    profile_dp = models.ImageField(upload_to = content_file_name, storage=OverwriteStorage(), null=True, blank=True)
    profile_url = models.CharField(max_length=200)

class Wallet(models.Model):
    user = models.ForeignKey(User,null=True,related_name='wallet_mobile',on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('Total amount'), max_digits=10, decimal_places=2, default=10)
    add_amount = models.DecimalField(_('Add amount'), max_digits=10, decimal_places=2, default=0)
    deposit_cash = models.DecimalField(_('Full Add amount'), max_digits=10, decimal_places=2, default=0)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    winning_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdraw_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)   
  

class ReferralRelationship(models.Model):
    # who invite 
    employer = models.ForeignKey(User,related_name='inviter',verbose_name="inviter",on_delete=models.CASCADE,)
    # who connected 
    employee = models.ForeignKey(User,related_name='invited',verbose_name="invited",on_delete=models.CASCADE,)
    # referral code
    refer_token = models.ForeignKey("ReferralCode",related_name="referral_code",verbose_name="referral_code",on_delete=models.CASCADE,)

class ReferralCode(models.Model):
    token = models.CharField(unique=True, max_length=150)
    user = models.ForeignKey(User, verbose_name="code_master", on_delete=models.CASCADE)