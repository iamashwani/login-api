from rest_framework import serializers
from .models import User, Wallet, ReferralCode, ReferralRelationship
import random
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from django.conf import settings
import base64
# from django.core.files.storage import default_stroage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'mobile','name','username','logo','profile_dp','profile_url']
        read_only_fields = ['id','name','username','logo','profile_dp','profile_url']

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
            # instance.profile_url = 
            instance.save()

           
                
            extension = random_logo.split(".")[-1]
            ext2 = random_logo.replace(extension, "png")
            og_filename = ext2.split('.')[0]
            og_filename2 = ext2.replace(og_filename, str(instance.id))
            # r = os.path.join('profile/', og_filename2)
            # pat=default_stroage.save(r,ContentFileName())
            instance.profile_url = 'http://127.0.0.1:8000/'+ og_filename2
            instance.profile_dp = og_filename2
            r = os.path.join('profile/', instance.profile_url)
            
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
        fields = ['user','total_amount','deposit_cash','winning_cash','withdraw_amount']

class walletserializer_add(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','deposit_cash','winning_cash']

class walletserializer_deduct(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','total_amount','deposit_cash','winning_cash','withdraw_amount']





class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralRelationship
        fields = ["employer","employee", "refer_token"]

class RefferCodeSerializer(serializers.ModelSerializer):
    referral_code = ReferralSerializer(many=True, default="")
    class Meta:
        model = ReferralCode
        fields = [ "token", "user", "referral_code"]