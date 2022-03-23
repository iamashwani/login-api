from rest_framework import serializers
from .models import *
import random
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ['mobile']

    def create(self, validated_data):
    
        instance = self.Meta.model(**validated_data)
        
        instance.otp = str(random.randint(1000 , 9999))
        instance.save()
        return instance

    # def otp(self):
    #     instance = self.Meta.model()
    #     return instance.otp
