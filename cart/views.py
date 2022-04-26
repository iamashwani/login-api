from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from .models import User,Wallet,Transaction,UserReferral,Wheel
from .serializers import ProfileSerializer, \
    VerifyOTPSerializer, UserProfileChangeSerializer,\
    GetTotalwalletserializer,UserGetProfileChangeSerializer,walletserializer_deduct,\
    walletserializer_add,GetResponceSerializer,TransactionHistoryserializer,\
    Transactionserializer,Getreferralserializer,Bonusserializer,RedeemReferralcodeserializer,\
    GetResponceRedeemSerializer,Bonusserializer12
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
import http.client
from django.http import HttpResponse, JsonResponse
import urllib.request as urllib2
# from .serializers import RefferCodeSerializer
# from rest_framework.generics import ListAPIView
# from .models import ReferralCode
import datetime
import random


def send_otp(mobile, otp):

    authkey = settings.AUTH_KEY
    url = "http://amazesms.in/api/pushsms?user=hogotp&authkey="+authkey+"&sender=AMTSHR&mobile="+mobile+"&text=Hi%20%2C%20Your%20OTP%20is%20"+otp+".%20Valid%20for%203min.%20AMTSHR&entityid=1201159141994639834&templateid=1507164906024124641&rpt=1"

    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    data = page.read()
    print(data.decode("utf-8"))


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    def post(self, request):
        try:
            mobile = request.data['mobile']
            data = User.objects.filter(mobile=mobile).first()
            referral = request.data.get('referral')
            data_ref = User.objects.filter(referral=referral).first()
            if data is not None:
                serializer = self.serializer_class(data=request.data)
                mobile = request.data['mobile']
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    content = {'status': True, 'message': 'success', 'id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                               'username': instance.username, 'profile_id': instance.profile_id}
                    mobile = instance.mobile
                    otp = instance.otp
                    send_otp(mobile, otp)
                    return JsonResponse(content, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'status': False, "message": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)

            elif data_ref:
                serializer = self.serializer_class(data=request.data)
                mobile = request.data['mobile']
                referral = request.data['referral']
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    content = {'status': True, 'message': 'success', 'id': instance.id, 'mobile': instance.mobile,
                               'otp': instance.otp, 'name': instance.name,
                               'username': instance.username, 'profile_id': instance.profile_id}
                    mobile = instance.mobile
                    otp = instance.otp
                    send_otp(mobile, otp)
                    wallet = 50
                    description = "Welcome bonus"
                    wall = Wallet.objects.create(user=instance, total_amount=wallet, description=description, )
                    wall.save()
                    transaction_history_obj = Transaction()
                    transaction_history_obj.transactiontype = "Referral Bonus"
                    obj = Transaction.objects.create(user=instance, amount=wallet, description=description, transactiontype=transaction_history_obj.transactiontype)
                    obj.save()
                    user = User.objects.filter(referral=request.user)
                    current_datetime = datetime.datetime.now()
                    user_referral = UserReferral.objects.update(referred_by=instance.id,joined_date=current_datetime)
                    return JsonResponse(content, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'status': False, "message": "Login in Failed"},status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.serializer_class(data=request.data)
                mobile = request.data['mobile']
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    content = {'status': True, 'message': 'success','id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                               'username': instance.username,'profile_id': instance.profile_id}
                    mobile = instance.mobile
                    otp = instance.otp
                    wallet = 50
                    description = "Welcome bonus"
                    wall = Wallet.objects.create(user=instance,total_amount=wallet,description=description,)
                    wall.save()
                    transaction_history_obj = Transaction()
                    transaction_history_obj.transactiontype = "Welcome Bonus"

                    obj = Transaction.objects.create(user=instance, amount=wallet, description=description,transactiontype=transaction_history_obj.transactiontype)
                    obj.save()
                    send_otp(mobile, otp)
                    return JsonResponse(content, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'status': False, "message": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request, id):
        try:
            serializer = VerifyOTPSerializer(data=request.data)
            otp_sent = request.data['otp']
            otp = User.objects.get(pk=id)
            if otp_sent:
                old = User.objects.filter(id=otp.id)
                if old is not None:
                    old = old.first()
                    otp = old.otp
                    if str(otp) == str(otp_sent):
                        return JsonResponse({'status': True,'message': 'OTP is correct'})
                    else:
                        return JsonResponse({'status': False,'message': 'OTP incorrect, please try again'})
        except:
            return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def Get_Profile(request, pk):
    try:
        if request.method == 'GET':
            snippet = User.objects.get(pk=pk)
            serializer = UserGetProfileChangeSerializer(snippet)
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET', 'POST'])
def Update_Profile(request,pk):

    if request.method == 'GET':
        snippet = User.objects.get(pk=pk)
        serializer = UserProfileChangeSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'POST':
        snippet = User.objects.get(pk=pk)
        serializer = UserProfileChangeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_wallet(request, pk):
    try:
        qs = Wallet.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = GetTotalwalletserializer(qs)
            # qs.total_amount = qs.total_amount + qs.winning_cash
            # qs.save()
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({"status": False, "message": "Something went wrong. Please try again later."}, status=404)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET', 'POST'])
def transactionmoney(request, pk):
    try:
        if request.method == 'POST':
            user = User.objects.get(pk=pk)
            qs = Wallet.objects.get(pk=pk)
            serializer = Transactionserializer(qs, data=request.data)
            if serializer.is_valid(raise_exception=True):
                amount = request.data['amount']
                qs.amount = amount
                description = request.data['description']
                qs.description = description
                if amount > 0:
                    qs.winning_cash = qs.winning_cash + amount
                    qs.total_amount = qs.total_amount + amount
                    qs.save()
                    transaction_history_obj = Transaction()
                    transaction_history_obj.transactiontype = "Credited amount"
                    obj = Transaction.objects.create(user=user, amount=qs.amount, description=description,
                                                     winning_cash=qs.winning_cash,transactiontype=transaction_history_obj.transactiontype)
                    obj.save()
                elif amount < 0:
                    qs.winning_cash = qs.winning_cash + amount
                    qs.total_amount = qs.total_amount + amount
                    qs.save()
                    transaction_history_obj = Transaction()
                    transaction_history_obj.transactiontype = "Debit Amount"
                    obj = Transaction.objects.create(user=user, amount=qs.amount,description=description,winning_cash=qs.winning_cash,transactiontype=transaction_history_obj.transactiontype)
                    obj.save()
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({"status": False, "message": "Something went wrong. Please try again later", },
                                status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET'])
def transactionsHistory(request,pk):
    try:
        if request.method == 'GET':
            wll = Wallet.objects.get(pk=pk)
            qs = Transaction.objects.filter(wallet=wll).order_by('-pk')
            serializer = TransactionHistoryserializer(qs)
            json_data = []
            for x in qs:
                json_data.append({
                    'id': x.pk,
                    'amount': x.amount,
                    'description': x.description,
                    'date': x.date,
                    'time': x.time,
                })
            return JsonResponse({"status": True, "message": "success", "data": json_data}, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({"status": False, "message": "Something went wrong. Please try again later"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def getreferral(request, pk):
    try:
        qs = User.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = Getreferralserializer(qs)
            if qs.referral is not None:
                json_data = serializer.data
                x = GetResponceSerializer(json_data)
                x = {**x.data, **json_data}
                return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse({'status': False, 'message': 'Referral Code Cannot Get'})
    except:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RedeemReferralcode(request, pk):
    try:
        qs = User.objects.get(pk=pk)
        wll = Wallet.objects.get(pk=pk)
        if request.method == 'POST':
            serializer = RedeemReferralcodeserializer(qs, data=request.data)
            if serializer.is_valid(raise_exception=True):
                referral = request.data['referral']
                if qs.referral == referral:
                    qs.referral_status = qs.referral
                    qs.referral_status = True
                    qs.save()
                    referral_datetime = datetime.datetime.now()
                    obj = UserReferral.objects.create(user=qs, referral_url=qs.referral,referral_date=referral_datetime)
                    obj.save()
                    wall = Wallet.objects.update(user=qs,Bonus=50, total_bonus_amount=wll.total_bonus_amount + 50)
                    transaction_history_obj = Transaction()
                    transaction_history_obj.transactiontype = 'Referral Bonus'
                    transaction_history_obj.user = qs
                    transaction_history_obj.amount = 50
                    transaction_history_obj.description = "Referral Bonus"
                    transaction_history_obj.save()
                    return JsonResponse({'status': True,'message': 'Redeemed Successfully'}, status=status.HTTP_200_OK, safe=False)
                else:
                    return JsonResponse({'status': False,'message': 'Referral Code Cannot Redeem'})
    except:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_wheel_details(request, id):
    if request.method == 'GET':
        qs = User.objects.get(pk=id)
        wellet = Wallet.objects.get(pk=id)
        serializer = Bonusserializer(qs, data=request.data)
        if serializer.is_valid(raise_exception=True):
            li = ['5 Rs. Entry ticket', 'Get Another Spin', '50 Rs Bonus', '10% Discount Coupon',
                  '20% Extra Referral Bonus', '5 Rs Bonus', 'Better luck next time', '10 Rs Bonus']
            x = random.randint(0, len(li) - 1)
            obj = Wheel.objects.create(user=qs,wheels_index=x, wallet=wellet)
            obj.save()
        return JsonResponse({"status": True, "message": "success","data":li, "winning_Index": x},safe=False)
    else:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later", },
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def claim_wheel_bonus(request, id):
    try:
        if request.method == 'POST':
            user = User.objects.get(pk=id)
            wheel = Wheel.objects.filter(user=id).order_by('-id')[0]
            qs = Wallet.objects.get(user=id)

            # wheel = Wheel.objects.get(pk=wheel_id)
            # user = User.objects.get(wheel=wheel_id)
            # qs = Wallet.objects.get(wheel=wheel_id)
            serializer = Bonusserializer12(qs, data=request.data)
            if serializer.is_valid(raise_exception=True):
                if wheel.wheels_index == '0':
                    qs.Bonus = qs.Bonus + 5
                    qs.total_amount = qs.total_amount + 5
                    qs.save()
                    obj = Transaction.objects.create(user=user, amount=5, description="5 Rs. Entry ticket",
                                                     transactiontype="claim_wheel_bonus")
                    obj.save()
                elif wheel.wheels_index == '1':
                    get_wheel_details()
                elif wheel.wheels_index == '2':
                    qs.Bonus = qs.Bonus + 50
                    qs.total_amount = qs.total_amount + 50
                    qs.save()
                    obj = Transaction.objects.create(user=user, amount=50, description="50 Rs Bonus", transactiontype = "claim_wheel_bonus")
                    obj.save()
                elif wheel.wheels_index == '3':
                    return JsonResponse({"status": True,"message": "10% Discount Coupon"})
                elif wheel.wheels_index == '4':
                    qs.Bonus = qs.Bonus + 10
                    qs.total_amount = qs.total_amount + 10
                    qs.save()
                    obj = Transaction.objects.create(user=user, amount=10, description="20% Extra Referral Bonus",transactiontype="claim_wheel_bonus")
                    obj.save()
                elif wheel.wheels_index == '5':
                    qs.Bonus = qs.Bonus + 5
                    qs.total_amount = qs.total_amount + 5
                    qs.save()
                    obj = Transaction.objects.create(user=user,amount=5, description="5 Rs Bonus",transactiontype="claim_wheel_bonus" )
                    obj.save()
                elif wheel.wheels_index == '6':
                    return JsonResponse({"status": False, "message": "Better luck next time"})
                elif wheel.wheels_index == '7':
                    qs.Bonus = qs.Bonus + 10
                    qs.total_amount = qs.total_amount + 10
                    qs.save()
                    obj = Transaction.objects.create(user=user, amount=10, description="10 Rs Bonus", transactiontype="claim_wheel_bonus")
                    obj.save()
                json_data = serializer.data
                x = GetResponceSerializer(json_data)
                x = {**x.data, **json_data}
                return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later"},
                            status=status.HTTP_400_BAD_REQUEST)

# if x == li[0]:
#     qs.Bonus = qs.Bonus + 5
#     qs.save()
#     # obj = Transaction.objects.create(user=user, wallet=qs, Bonus=qs.Bonus, description=x,)
#     # obj.save()
# elif x == li[1]:
#     y = 'Get Another Spin'
#     return y
# elif x == li[2]:
#     qs.Bonus = qs.Bonus + 50
#     qs.save()
#     # obj = Transaction.objects.create(user=user, wallet=qs, Bonus=qs.Bonus, description=x, )
#     # obj.save()
# elif x == li[3]:
#     y = "10% Discount Coupon"
#     return y
# elif x == li[4]:
#     y = "Better luck next time"
#     return y
# elif x == li[5]:
#     qs.Bonus = qs.Bonus + 5
#     qs.save()
#     # obj = Transaction.objects.create(user=user, wallet=qs, Bonus=qs.Bonus, description=x, )
#     # obj.save()
# elif x == li[6]:
#     y = "Better luck next time"
#     return y
# elif x == li[7]:
#     qs.Bonus = qs.Bonus + 10
#     qs.save()
# obj = Wallet.objects.create(wallet=qs,Bonus = qs.Bonus)
# obj.save()
# json_data = x
# y = GetResponceSerializer(json_data)
# y = {**y.data, **json_data}

# @api_view(['GET'])
# def total_of_add_money(request,pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer(qs)
#             qs.total_amount = qs.total_amount + qs.add_amount
#             qs.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response('')
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                             status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
# @api_view(['GET'])
# def total_of_win_money(request,pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer(qs)
#             qs.total_amount = qs.total_amount + qs.win_amount
#             qs.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response('')
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                             status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#
#
# @api_view(['GET'])
# def full_money(request, pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer_add(qs)
#             qs.deposit_cash = qs.deposit_cash + qs.add_amount
#             qs.winning_cash = qs.winning_cash + qs.win_amount
#             qs.save()
#             json_data = serializer.data
#             x = GetResponceSerializer(json_data)
#             x = {**x.data, **json_data}
#             return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
#         else:
#             return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                         status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#
# @api_view(['GET'])
# def withdraw_amount(request, pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer_deduct(qs)
#             if qs.winning_cash > qs.withdraw_amount:
#                 qs.winning_cash = qs.winning_cash - qs.withdraw_amount
#                 qs.total_amount = qs.total_amount - qs.withdraw_amount
#                 qs.save()
#                 json_data = serializer.data
#                 x = GetResponceSerializer(json_data)
#                 x = {**x.data, **json_data}
#                 return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
#             else:
#                 return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                     status=status.HTTP_503_SERVICE_UNAVAILABLE)