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
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile
import pyotp
import random

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['mobile']
    def create(self, validated_data):
        
            instance = self.Meta.model(**validated_data)
            global totp
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret, interval=300)
            otp = totp.now()
            instance.otp = str(random.randint(1000 , 9999))
            instance.save()
            return instance

class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=255)
    # username = serializers.CharField(max_length=255, read_only=True)
    otp = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        fields = ('mobile','otp','token')

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['mobile','otp']