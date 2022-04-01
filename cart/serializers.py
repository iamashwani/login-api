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

from .models import User
import pyotp
import random
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile']
    def create(self, validated_data):
        
        #instance = self.Meta.model(**validated_data)
        global totp
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=300)
        otp = totp.now()
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords,k = 6)))
        # path = os.path.join(BASE_DIR, 'static')
        # dir_list = os.listdir(path)
        # random_logo = random.choice(dir_list)

        instance = User.objects.bulk_create(validated_data,dict(otp=str(otp),username = res,name = res , profile_id = res))[0]            
        instance.save()
        return instance
# logo = instance.logo
    def update(self,instance, validated_data):
        instance.otp = validated_data.get('otp', instance.otp)
        instance.save()
        return instance


class VerifyOTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['mobile','otp']
        
    # def create(self,validated_data):
        
    #     instance = self.Meta.model(**validated_data)
    #     mywords = "123456789"
    #     res = "expert@" + str(''.join(random.choices(mywords,k = 6)))
      
    #     path = os.path.join(BASE_DIR, 'static')
    #     dir_list = os.listdir(path)
    #     random_logo = random.choice(dir_list)
        
    #     instance = self.Meta.model.objects.update_or_create(**validated_data, defaults = dict(username = res,name = instance.mobile ,logo = random_logo, profile_id = res))[0]
    #     instance.save()
    #     return instance
    


         

