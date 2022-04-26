from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import os
from cart.storage import OverwriteStorage
from .managers import SoftDeletionManager


class SoftDeleteModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, default=1)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.IntegerField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    deleted_by = models.IntegerField(null=True, blank=True, default=None)
    deleted_on = models.DateTimeField(null=True, default=None, blank=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_on = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()


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
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200,null=True, blank=True,)
    username = models.CharField(max_length=200,null=True, blank=True,)
    profile = models.ImageField(upload_to=content_file_name, storage=OverwriteStorage(), blank=True)
    profile_id = models.IntegerField(default=0)
    referral = models.CharField(max_length=150,null=True, blank=True,)
    # referral_status = models.BooleanField(null=True, blank=True)



class Wallet(models.Model):
    user = models.ForeignKey(User, null=True, related_name='wallet_mobile', on_delete=models.CASCADE)
    # wallet = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.FloatField(_('Total amount'), default=10)
    add_amount = models.FloatField(_('Add amount'), default=0)
    deposit_cash = models.FloatField(_('Full Add amount'),default=0)
    win_amount = models.FloatField(default=0)
    winning_cash = models.FloatField(default=0)
    withdraw_amount = models.FloatField(default=0)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=200, null=True, blank=True, )
    total_bonus_amount = models.FloatField(default=0)
    Bonus = models.FloatField(default=0)


class Transaction(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    # wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transactiontype = models.CharField(max_length=200,blank=True,)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=200,blank=True,)
    winning_cash = models.FloatField(default=0)
    date = models.DateField(null=True, auto_now_add=True)
    time = models.TimeField(null=True, auto_now_add=True)


class UserReferral(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,related_name="user_referral_user")
    referred_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,related_name="user_referred_by_user")
    joined_date = models.DateTimeField(null=True, blank=True)
    referral_date = models.DateTimeField(null=True, blank=True)
    referral_url = models.CharField(max_length=500, null=True, blank=True)
    # referral_resource = models.CharField(max_length=500, null=True, blank=True)


class Wheel(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet,null=True, on_delete=models.CASCADE)
    wheels_index = models.CharField(max_length=200, null=True, blank=True)