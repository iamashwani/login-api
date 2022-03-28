# from rest_framework import serializers
# from .models import *
# import random
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Profile
#         fields = ['mobile']

#     def create(self, validated_data):
    
#         instance = self.Meta.model(**validated_data)
        
#         instance.otp = str(random.randint(1000 , 9999))
#         instance.save()
#         return instance

# class VerifyOTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['otp', 'mobile']

#     # def otp(self):
#     #     instance = self.Meta.model()
#     #     return instance.otp
from email.policy import default
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import pyotp
import random
import os
from django.db.models import Q
from django.conf import settings
from django.conf.urls.static import static
from pathlib import Path
from django.core.files.storage import FileSystemStorage
BASE_DIR = Path(__file__).resolve().parent.parent
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile']
    def create(self, validated_data):
        
            instance = self.Meta.model(**validated_data)
            global totp
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret, interval=300)
            otp = totp.now()
            instance = self.Meta.model.objects.update_or_create(**validated_data, defaults=dict(otp=str(random.randint(1000 , 9999))))[0]            
            instance.save()
            return instance

#from django.core.files.base import ContentFile
class VerifyOTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['mobile','otp']
        
    def create(self,validated_data):
        
        instance = self.Meta.model(**validated_data)
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords,k = 6)))
        # path = os.path.join(BASE_DIR, 'static')
        # random_logo = random.choice([ x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
        #BASE_DIR = Path(__file__).resolve().parent.parent
        path = os.path.join(BASE_DIR, 'static')
        dir_list = os.listdir(path)
        random_logo = random.choice(dir_list)
        # file ='logo/'
        # fs = FileSystemStorage(location = file)
        # filename = fs.save(random_logo)
        # file_url = fs.url(filename,)
        instance = self.Meta.model.objects.update_or_create(**validated_data, defaults = dict(username = res,name = instance.mobile ,logo = random_logo, profile_id = res))[0]
        instance.save()
        return instance


         

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'debit_or_credit', 'transaction_amount', 'curr_available_amount_if_credit_row',
                  'transaction_method_record_unique_id','transaction_time',
                  'wallet_debit_record2wallet_credit_record','wallet2store_details','hmac_or_checksum','is_deleted')
