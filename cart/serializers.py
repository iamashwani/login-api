from email.policy import default
from rest_framework import serializers

from .models import User,Wallet
import pyotp
import random
import os

from pathlib import Path
from django.core import files
from django.core.files.base import ContentFile

BASE_DIR = Path(__file__).resolve().parent.parent
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.templatetags.static import static
import pandas as pd


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile', 'name', 'username', 'logo']
        read_only_fields = ['id','name', 'username', 'logo']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords, k=6)))
        path = os.path.join(BASE_DIR, 'static/images')
        dir_list = os.listdir(path)
        random_logo = random.choice(dir_list)

        if self.Meta.model.objects.filter(**validated_data).exists():
            instance = self.Meta.model.objects.filter(**validated_data).last()
            instance.otp = str(random.randint(1000, 9999))
            instance.save()
        else:
            instance = self.Meta.model(**validated_data)
            instance.otp = str(random.randint(1000, 9999))
            instance.username = res
            instance.name = instance.mobile
            instance.logo = random_logo
            instance.profile_id = random_logo
            instance.id = instance.id

            instance.save()
        return instance


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp', 'id']
        # read_only_fields = ['mobile']


class UserProfileChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'logo']


class walletserializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'total_amount', 'add_amount', 'win_amount', 'deduct_amount']

