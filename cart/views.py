from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User,Wallet
from .serializers import ProfileSerializer, VerifyOTPSerializer, UserProfileChangeSerializer,walletserializer
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
                content = {'mobile': instance.mobile, 'otp': instance.otp}
                mobile = instance.mobile
                otp = instance.otp
                send_otp(mobile, otp)
                return JsonResponse(content, status=status.HTTP_201_CREATED,safe=False)
            else:
                return JsonResponse({"Error": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                content = {'id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                           'username': instance.username, 'logo': instance.logo, 'profile_id': instance.profile_id}
                mobile = instance.mobile
                otp = instance.otp
                wallet = 10
                wall = Wallet.objects.create(user=instance,total_amount=wallet)
                send_otp(mobile, otp)
                return JsonResponse(content, status=status.HTTP_201_CREATED, safe=False)
            else:
                return JsonResponse({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)


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
                    return JsonResponse({'status': True,'detail': 'OTP is correct'},safe=False)
                else:
                    return JsonResponse({'status': False,'detail': 'OTP incorrect, please try again'})


@api_view(['GET'])
def Get_Profile(request, pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserProfileChangeSerializer(snippet)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
def Update_Profile(request,pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserProfileChangeSerializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        serializer = UserProfileChangeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_wallet(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        return JsonResponse(serializer.data, status=200)
    return JsonResponse({"Something went wrong. Please try again later."}, status=404)


@api_view(['GET','PUT'])
def add_money(request,pk):
    # import pdb
    # pdb.set_trace()
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
        qs.save()
        return JsonResponse(serializer.data, status=200)