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
from django.core import files
from django.core.files.base import ContentFile
BASE_DIR = Path(__file__).resolve().parent.parent
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile','name','username','logo']
        read_only_fields = ['name','username','logo']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)      
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords,k = 6)))
        path = os.path.join(BASE_DIR, 'static\images')
        dir_list = os.listdir(path, )
        random_logo = random.choice(dir_list)
       
        if self.Meta.model.objects.filter(**validated_data).exists():
            instance = self.Meta.model.objects.filter(**validated_data).last()          
            instance.otp = str(random.randint(1000 , 9999))
            instance.save()
        else:
            instance = self.Meta.model(**validated_data)
            instance.otp = str(random.randint(1000 , 9999))
            instance.username = res
            instance.name = instance.mobile
            instance.logo = random_logo
            instance.profile_id = res
            instance.save()
        return instance

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'otp']

# class UpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('mobile','name','username','logo')

#     def validate_mobile(self, mobile):
#         user = self.context['request'].user
#         mobile = self.context['request'].mobile
#         if User.objects.exclude(pk=user.pk).filter(mobile=mobile).exists():
#             raise serializers.ValidationError({"email": "This mobile is already in use."})
#         return mobile

#     def validate_username(self, username):
#         user = self.context['request'].user
#         username = self.context['request'].username
#         if User.objects.exclude(pk=user.pk).filter(username=username).exists():
#             raise serializers.ValidationError({"username": "This username is already in use."})
#         return username
        
#     def validate_name(self, name):
#         user = self.context['request'].user
#         name = self.context['request'].name
#         if User.objects.exclude(pk=user.pk).filter(name=name).exists():
#             raise serializers.ValidationError({"username": "This name is already in use."})
#         return name
#     def validate_logo(self, logo):
#         user = self.context['request'].user
#         logo = self.context['request'].logo
#         if User.objects.exclude(pk=user.pk).filter(logo=logo).exists():
#             raise serializers.ValidationError({"username": "This logo is already in use."})
#         return logo
#     def update(self, instance, validated_data):
#             user = self.context['request'].user

#             if user.mobile== instance.mobile:
#                 raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

#             instance.mobile = validated_data['mobile']
#             instance.name = validated_data['name']
#             instance.logo = validated_data['logo']
#             instance.username = validated_data['username']

#             instance.save()

#             return instance

class UserProfileChangeSerializer(serializers.ModelSerializer):
	# class Meta:
	# 	model = User
	# 	fields = [
    #         'name','username','logo'
    #     ]
    
    class Meta:
        model = User
        fields = [
            'name','username','logo'
        ]

    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username')
    #     instance.name = validated_data.get('name')
    #     instance.logo = validated_data.get('logo')
        
    #     instance.save()
    #     return instance 




