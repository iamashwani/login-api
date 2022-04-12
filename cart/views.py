from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User,Wallet
from .serializers import ProfileSerializer, \
    VerifyOTPSerializer, UserProfileChangeSerializer,\
    walletserializer,UserGetProfileChangeSerializer,walletserializer_deduct,\
    walletserializer_add,GetProfileResponceSerializer
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
import requests
from rest_framework import generics, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
import http.client
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.views import exception_handler

#
def api_500_handler(exception, context):
    response = exception_handler(exception, context)
    try:
        detail = response.data['detail']
    except AttributeError:
        detail = exception.message
    response = HttpResponse(
        json.dumps({'detail': detail}),
        content_type="application/json", status=500
    )
    return response


# def error_404_view(request,exception):
#     return HttpResponse("invalid")


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
                content = {'status': True, 'message': 'success', 'id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                           'username': instance.username, 'profile_url': instance.profile_url, 'profile_id': instance.profile_id}
                mobile = instance.mobile
                otp = instance.otp
                send_otp(mobile, otp)
                return JsonResponse(content, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'status': False, "message": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                content = {'status': True, 'message': 'success','id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                           'username': instance.username, 'profile_url': instance.profile_url, 'profile_id': instance.profile_id}
                mobile = instance.mobile
                otp = instance.otp
                wallet = 10
                wall = Wallet.objects.create(user=instance,total_amount=wallet)
                send_otp(mobile, otp)
                return JsonResponse(content, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'status': False, "message": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request,id):
        # import pdb
        # pdb.set_trace()
        serializer = VerifyOTPSerializer(data=request.data)
        # mobile = request.data['mobile']
        otp_sent = request.data['otp']
        otp = User.objects.get(pk=id)
        if otp_sent:
            old = User.objects.filter(id=otp.id)
            if old is not None:
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    return JsonResponse({'status': True,'detail': 'OTP is correct'})
                else:
                    return JsonResponse({'status': False,'detail': 'OTP incorrect, please try again'})


@api_view(['GET'])
def Get_Profile(request, pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserGetProfileChangeSerializer(snippet)
        return JsonResponse({"status": True, "message": "success", "data": serializer.data}, status=status.HTTP_200_OK, safe=False)



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
            return JsonResponse({'status': 'True',"message": "success", 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_wallet(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        return JsonResponse({"status": True, "message": "success", "data": serializer.data}, status=200, safe=False)
    else:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later."}, status=404)


# @api_view(['GET'])
# def total_money(request, pk):
#     qs = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = walletserializer(qs)
#         qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
#         qs.save()
#         return JsonResponse({"status": "success", "data":serializer.data}, status=True)
#
#
# @api_view(['GET'])
# def full_money(request, pk):
#     qs = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = walletserializer_add(qs)
#         qs.full_add_amount = qs.full_add_amount + qs.add_amount
#         qs.full_win_amount = qs.full_win_amount + qs.win_amount
#         qs.save()
#         return JsonResponse(serializer.data,status=status.HTTP_200_OK, safe=False)
#     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def deduct_amount(request, pk):
#     qs = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = walletserializer_deduct(qs)
#         if qs.full_win_amount > qs.deduct_amount:
#             qs.full_win_amount = qs.full_win_amount - qs.deduct_amount
#             qs.total_amount = qs.total_amount - qs.deduct_amount
#             qs.save()
#             return Response(serializer.data, status=200)
#         else:
#             return Response({"Not have enough balance"})