from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers
from .models import Wallet


class WalletDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('id', 'mobile', 'balance')