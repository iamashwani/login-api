from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import exceptions
from django.conf import settings
from django.db import transaction
from base.renderers import custom_response_renderer


class DepositAmount(APIView):
    # permission_classes = (IsAuthenticated, )
    def post(self, request):
        amount = request.data.get('amount', None)
        success, error_msg, data = True, None, {}
        if (not amount) or (amount <= 0):
            success = False
            error_msg = "Invalid amount."
        wallet = request.user.get_wallet()

        if amount:
            with transaction.atomic():
                wallet.deposit(amount)
        return custom_response_renderer(
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


