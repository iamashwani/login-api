from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User,Wallet
from .serializers import ProfileSerializer, VerifyOTPSerializer, \
    UserProfileChangeSerializer,walletserializer,UserGetProfileChangeSerializer,\
    walletserializer_deduct,walletserializer_add

from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
import requests
from rest_framework import generics, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
import http.client
from django.http import HttpResponse, JsonResponse


def send_otp(mobile, otp):
    url = http.client.HTTPConnection("2factor.in")
    authkey = settings.AUTH_KEY
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }
    url.request("GET", "/API/V1/"+str(authkey)+"/SMS/"+str(mobile)+"/"+str(otp),payload, headers)
    res = url.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    def post(self, request):
        mobile = request.data['mobile']
        data = User.objects.filter(mobile=mobile).first()
        if data is not None:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                content = {'id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                           'username': instance.username, 'profile_url': instance.profile_url, 'profile_id': instance.profile_id}
                mobile = instance.mobile
                otp = instance.otp
                send_otp(mobile, otp)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                content = {'id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                           'username': instance.username, 'profile_url': instance.profile_url, 'profile_id': instance.profile_id}
                mobile = instance.mobile
                otp = instance.otp
                wallet = 10
                wall = Wallet.objects.create(user=instance,total_amount=wallet)
                send_otp(mobile, otp)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        # mobile = request.data['mobile']
        otp_sent = request.data.get('otp',False)
        mobile = request.data.get('mobile',False)

        # user_id = User.objects.get(pk=id)
        if mobile and otp_sent:
            old = User.objects.filter(mobile__iexact=mobile)
            if old is not None:
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    return Response({'status': True,'detail': 'OTP is correct'})
                else:
                    return Response({'status': False,'detail': 'OTP incorrect, please try again'})


@api_view(['GET'])
def Get_Profile(request, pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserGetProfileChangeSerializer(snippet)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
def Update_Profile(request,pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserProfileChangeSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserProfileChangeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_wallet(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        return Response(serializer.data, status=200)
    return Response({"Something went wrong. Please try again later."}, status=404)



@api_view(['GET'])
def total_money(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
        qs.save()
        return Response(serializer.data, status=200)


@api_view(['GET'])
def full_add_money(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer_add(qs)
        qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
        qs.total_add_amount = qs.total_add_amount + qs.add_amount

        qs.save()
        return Response(serializer.data, status=200)

@api_view(['GET'])
def win_money(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer_add(qs)
        qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
        qs.total_win_amount = qs.total_win_amount+ qs.win_amount
        qs.save()
        return Response(serializer.data, status=200)


@api_view(['GET'])
def deduct_amount(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer_deduct(qs)
        if qs.total_win_amount > qs.deduct_amount:
            qs.total_win_amount = qs.total_win_amount - qs.deduct_amount
            qs.total_amount = qs.total_amount - qs.deduct_amount
            qs.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"Not have enough balance"})
