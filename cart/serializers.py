from rest_framework import serializers
from .models import User, Wallet
import random
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from django.conf import settings
import base64
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'mobile','name','username','logo','profile_dp']
        read_only_fields = ['id','name','username','logo','profile_dp']

    def create(self, validated_data):
      
        instance = self.Meta.model(**validated_data)      
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords,k = 6)))
        path = os.path.join(BASE_DIR, 'static/images')
        dir_list = os.listdir(path)
        random_logo = random.choice(dir_list)
        
        if self.Meta.model.objects.filter(**validated_data).exists():
            instance = self.Meta.model.objects.filter(**validated_data).last()          
            instance.otp = str(random.randint(100000 , 999999))
            instance.save()
        else:
            instance = self.Meta.model(**validated_data)
            instance.otp = str(random.randint(100000 , 999999))
            instance.username = res
            instance.name = instance.mobile
            instance.logo = random_logo
            instance.profile_url = res
            instance.save()
        return instance

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'otp']
        read_only_fields = ['mobile']
class UserProfileChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','username','logo']  

class walletserializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','total_amount','deposit_cash','winning_cash','deduct_amount']

class walletserializer_add(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','deposit_cash','winning_cash']

class walletserializer_deduct(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','total_amount','deposit_cash','winning_cash','deduct_amount']



