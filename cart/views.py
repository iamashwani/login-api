# from tkinter import NONE
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render , redirect

# from django.contrib.auth.models import User

# from .models import Profile
# import random

# import http.client
# import requests

# from django.conf import settings
# from django.contrib.auth import authenticate, login
# from rest_framework.parsers import JSONParser
# from .serializers import *
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status

# # Create your views here.


# def send_otp(mobile,otp):
#     url = "https://www.fast2sms.com/dev/bulkV2"
#     authkey = settings.AUTH_KEY
#     querystring = {"authorization":authkey,"variables_values":otp,"route":"otp","numbers":mobile}

#     headers = {
#         'cache-control': "no-cache"
#     }

#     response = requests.request("GET", url, headers=headers, params=querystring)

#     print(response.text)
    



# # # def login_attempt(request):
# # #     if request.method == 'POST':
# # #         mobile = request.POST.get('mobile')
        
# # #         user = Profile.objects.filter(mobile = mobile).first()
        
# # #         if user is None:
# # #             context = {'message' : 'User not found' , 'class' : 'danger' }
# # #             return render(request,'cart/login.html' , context)
        
# # #         otp = str(random.randint(1000 , 9999))
# # #         user.otp = otp
# # #         user.save()
# # #         send_otp(mobile , otp)
# # #         request.session['mobile'] = mobile
# # #         return redirect('login_otp')        
# # #     return render(request,'cart/login.html')


# # def login_otp(request):
# #     mobile = request.session['mobile']
# #     context = {'mobile':mobile}
# #     if request.method == 'POST':
# #         otp = request.POST.get('otp')
# #         user = Profile.objects.filter(mobile=mobile).first()
        
# #         if otp == user.otp:
# #             return redirect('cart')
# #         else:
# #             context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
# #             return render(request,'cart/login_otp.html' , context)
    
# #     return render(request,'cart/login_otp.html' , context)
    
    
# @api_view(["POST"])
# def register(request):
    
#     if request.method == 'POST':
#         serializer = ProfileSerializer(data = request.data)
#         mobile = request.data['mobile']
#         check = Profile.objects.filter(mobile=mobile).first()
#         if check is not None:
#             if request.method == 'POST':
#                 serializer = ProfileSerializer(data = request.data)
#                 if serializer.is_valid():
#                     instance = serializer.save()
#                     content = {'mobile': instance.mobile, 'otp': instance.otp}
#                     mobile = instance.mobile
#                     otp = instance.otp
#                     send_otp(mobile,otp)
#                     print("Success")
#                     return Response(content, status=status.HTTP_201_CREATED)
        
#         if serializer.is_valid():
#             instance = serializer.save()
#             content = {'mobile': instance.mobile, 'otp': instance.otp}
#             mobile = instance.mobile
#             otp = instance.otp
#             send_otp(mobile,otp)
#             return Response(content, status=status.HTTP_201_CREATED)
        
# @api_view(['POST','GET'])
# def otp(request):
#     import pdb
#     pdb.set_trace()
#     #context = {'mobile':mobile}
#     if request.method == 'POST':
#         serializer = VerifyOTPSerializer(data = request.data)
        
#         if serializer.is_valid():
#             #mobile = request.data['mobile']
#             otp = request.data['otp']
#             profile = Profile.objects.filter(otp = otp).first()
        
#             if otp == profile:
#                 return Response( status=status.HTTP_201_CREATED)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
            
        
#         #return Response(status=status.HTTP_201_CREATED)

# #def verifyotp(otp,profile):


# # def otp(request):
# #     # mobile = request.session['mobile']
# #     # context = {'mobile':mobile}
# #     if request.method == 'POST':
# #         #otp = request.POST.get('otp')
# #         serializer = ProfileSerializer(data = request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             otp = request.data[otp]
# #             profile = Profile.objects.filter(otp = otp).first()
        
# #             if otp == profile:
# #                 return Response(serializer.data, status=status.HTTP_201_CREATED)
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
#     #return render(request,'cart/otp.html' , context)

# # def index(request):
# #     return HttpResponse(request,"cart/cart.html")

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import pyotp
import random
import jwt
from django.conf import settings

from .models import Profile
from .serializers import ProfileSerializer, VerifyOTPSerializer
from django.contrib.auth import authenticate
from passlib.hash import django_pbkdf2_sha256 as handler
#from rest_framework_simplejwt.serializers import VerifyJSONWebTokenSerializer
# from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.settings import api_settings
# from django.contrib.auth.models import update_last_login

from django.views.generic import View

import requests

# def generateOTP():
#     global totp
#     secret = pyotp.random_base32()
#     # set interval(time of the otp expiration) according to your need in seconds.
#     totp = pyotp.TOTP(secret, interval=300)
#     one_time = totp.now()
#     return one_time

# verifying OTP


# def verifyOTP(request):
#     mobile = request.data.get('mobile')
#     otp_sent  = request.data.get('otp')
#     if mobile and otp_sent:
#         old = Profile.objects.filter(mobile = mobile)
#         if old is not None:
#             old = old.first()
#             otp = old.otp
#             if str(otp) == str(otp_sent):
#                  return Response({
#                         'status' : True, 
#                         'detail' : 'OTP matched, kindly proceed to save password'
#                     })
#             else:
#                     return Response({
#                         'status' : False, 
#                         'detail' : 'OTP incorrect, please try again'
#                     })
                
def send_otp(mobile,otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    authkey = settings.AUTH_KEY
    querystring = {"authorization":authkey,"variables_values":otp,"route":"otp","numbers":mobile}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)



class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
    def post(self, request):
        mobile = request.data['mobile']
        data = Profile.objects.filter(mobile = mobile).first()
        if data is not None:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                content = {'mobile': instance.mobile, 'otp': instance.otp}
                mobile = instance.mobile
                otp = instance.otp
                print("Success")
                send_otp(mobile,otp)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
               
                instance = serializer.save()
                content = {'mobile': instance.mobile, 'otp': instance.otp}
                mobile = instance.mobile
                otp = instance.otp
                send_otp(mobile,otp)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        mobile = request.data['mobile']
        otp_sent = request.data['otp']
        #print('one_time_password', one_time)
        if mobile and otp_sent:
            old = Profile.objects.filter(mobile = mobile)
            if old is not None:
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    serializer = self.serializer_class(data=request.data)
                    mobile = request.data['mobile']
                    if serializer.is_valid(raise_exception=True):
                        instance = serializer.save()
                        content = {'mobile': instance.mobile, 'otp': instance.otp, 'name':instance.name, 'username':instance.username, 'logo':instance.logo, 'profile_id': instance.profile_id }
                        return Response(content, status=status.HTTP_201_CREATED)
                else:
                        return Response({
                            'status' : False, 
                            'detail' : 'OTP incorrect, please try again'
                        })


