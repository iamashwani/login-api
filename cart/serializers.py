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
        fields = ['mobile']

    # def create(self, validated_data):
    #     # import pdb
    #     # pdb.set_trace()
    #     instance = self.Meta.model(**validated_data)
    #     global totp
    #     secret = pyotp.random_base32()
    #     totp = pyotp.TOTP(secret, interval=300)
    #     otp = totp.now()
    #     mywords = "123456789"
    #     res = "expert@" + str(''.join(random.choices(mywords, k=6)))
    #     path = os.path.join(BASE_DIR, 'static\images')
    #     dir_list = os.listdir(path,)
    #     random_logo = random.choice(dir_list,)
    #     instance = User.objects.create(**validated_data,otp=otp,username=res, name=instance.mobile,
    #                                                                       logo=random_logo, profile_id=res, )[0]
    #     instance.save()
    #     return

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        global totp
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=300)
        otp = totp.now()
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords, k=6)))
        path = os.path.join(BASE_DIR, 'static\images')
        dir_list = os.listdir(path, )
        random_logo = random.choice(dir_list)


        mobile = validated_data.pop('mobile')
        obj = User.objects.create(**validated_data,otp=otp,username=res, name=mobile,logo=random_logo
                                                                          )
        return obj




    def update(self, instance, validated_data):
        mobile = validated_data.pop('mobile')
        albums = (instance.mobile).all()
        albums = list(albums)

        instance.save()


# from django.core.files.base import ContentFile
class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'otp']




