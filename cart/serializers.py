from email.policy import default
from rest_framework import serializers
from .models import User,Wallet,Transcations
import pyotp
import random
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile', 'name', 'username','profile_id','profile']
        read_only_fields = ['id','name', 'username', 'profile_id','profile']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        mywords = "123456789"
        res = "expert@" + str(''.join(random.choices(mywords, k=6)))
        # path = os.path.join(BASE_DIR, 'static/images')
        # dir_list = os.listdir(path)
        # random_logo = random.choice(dir_list)

        if self.Meta.model.objects.filter(**validated_data).exists():
            instance = self.Meta.model.objects.filter(**validated_data).last()
            instance.otp = str(random.randint(1000, 9999))
            instance.save()
        else:
            instance = self.Meta.model(**validated_data)
            instance.otp = str(random.randint(1000, 9999))
            instance.username = res
            instance.name = instance.mobile
            instance.profile_id = instance.profile_id
            instance.profile = instance.profile
            instance.id = instance.id
            instance.save()
            # path = os.path.join(BASE_DIR, 'static/images')
            # dir_list = os.listdir(path)
            # random_logo = random.choice(dir_list)
            #
            # extension = random_logo.split(".")[-1]
            # ext2 = random_logo.replace(extension, "png")
            # og_filename = ext2.split('.')[0]
            # og_filename2 = ext2.replace(og_filename, str(instance.id))
            # # import pdb
            # # pdb.set_trace()
            #
            # user_folder = 'static/images/profile/'
            # if not os.path.exists(user_folder):
            #     os.mkdir(user_folder)
            #
            # img_save_path = "%s/%s" % (user_folder, og_filename2)
            # with open(img_save_path, 'wb+') as f:
            #     for chunk in og_filename2.chunks():
            #         f.write(chunk)
            #     f.close()
            # instance.profile = 'profile/'+og_filename2
            # instance.save()
        return instance


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp']
        # read_only_fields = ['mobile']


class UserGetProfileChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'profile_url', 'profile_id']


class UserProfileChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','username', 'profile', 'profile_id']


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


class GetResponceSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    def get_status(self, obj):
        return True

    def get_message(self, obj):
        return "success"


class Transcationserializer(serializers.ModelSerializer):
    class Meta:
        model = Transcations
        fields = ['amount', 'description', 'total_amount']


class TranscationHistoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Transcations
        fields = ['wallet', 'amount', 'description']
        read_only_fields = ('wallet',)

