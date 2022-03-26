from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
# Create your models here.
from django.utils.crypto import get_random_string


class Profile(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    logo = models.ImageField(upload_to ='profile/', blank=True,null = True)
    profile_id = models.CharField(max_length=200)


class Wallet(models.Model):
    mobile = models.ForeignKey(Profile,null=True, on_delete=models.CASCADE)
    balance = models.DecimalField(
        _('Wallet Balance'), max_digits=10, decimal_places=2, default=0
    )
