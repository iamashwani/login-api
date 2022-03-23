from tkinter import NONE
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render , redirect

from django.contrib.auth.models import User

from .models import Profile
import random

import http.client
import requests

from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.


def send_otp(mobile,otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    authkey = settings.AUTH_KEY
    querystring = {"authorization":authkey,"variables_values":otp,"route":"otp","numbers":mobile}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    



# # def login_attempt(request):
# #     if request.method == 'POST':
# #         mobile = request.POST.get('mobile')
        
# #         user = Profile.objects.filter(mobile = mobile).first()
        
# #         if user is None:
# #             context = {'message' : 'User not found' , 'class' : 'danger' }
# #             return render(request,'cart/login.html' , context)
        
# #         otp = str(random.randint(1000 , 9999))
# #         user.otp = otp
# #         user.save()
# #         send_otp(mobile , otp)
# #         request.session['mobile'] = mobile
# #         return redirect('login_otp')        
# #     return render(request,'cart/login.html')


# def login_otp(request):
#     mobile = request.session['mobile']
#     context = {'mobile':mobile}
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         user = Profile.objects.filter(mobile=mobile).first()
        
#         if otp == user.otp:
#             return redirect('cart')
#         else:
#             context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
#             return render(request,'cart/login_otp.html' , context)
    
#     return render(request,'cart/login_otp.html' , context)
    
    
@api_view(["POST"])
def register(request):
    
    if request.method == 'POST':
        serializer = ProfileSerializer(data = request.data)
        mobile = request.data['mobile']
        check = Profile.objects.filter(mobile=mobile).first()
        if check is not None:
            if request.method == 'POST':
                serializer = ProfileSerializer(data = request.data)
                if serializer.is_valid():
                    instance = serializer.save()
                    content = {'mobile': instance.mobile, 'otp': instance.otp}
                    mobile = instance.mobile
                    otp = instance.otp
                    send_otp(mobile,otp)
                    print("Success")
                    return Response(content, status=status.HTTP_201_CREATED)
        
        if serializer.is_valid():
            instance = serializer.save()
            content = {'mobile': instance.mobile, 'otp': instance.otp}
            mobile = instance.mobile
            otp = instance.otp
            send_otp(mobile,otp)
            return Response(content, status=status.HTTP_201_CREATED)
        
@api_view(['POST'])
def otp(request):
    
    #context = {'mobile':mobile}
    if request.method == 'POST':
        serializer = ProfileSerializer(data = request.data)
        if serializer.is_valid():
            mobile = request.data['mobile']
            otp = request.data['otp']
            profile = Profile.objects.filter(mobile = mobile).first()
        
            if otp == profile.otp:
                return Response( status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        
        return Response(status=status.HTTP_201_CREATED)

# def otp(request):
#     # mobile = request.session['mobile']
#     # context = {'mobile':mobile}
#     if request.method == 'POST':
#         #otp = request.POST.get('otp')
#         serializer = ProfileSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             otp = request.data[otp]
#             profile = Profile.objects.filter(otp = otp).first()
        
#             if otp == profile:
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
    #return render(request,'cart/otp.html' , context)

# def index(request):
#     return HttpResponse(request,"cart/cart.html")

