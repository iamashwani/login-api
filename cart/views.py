from django.http import HttpResponse
from django.shortcuts import render , redirect

from django.contrib.auth.models import User

from .models import Profile
import random

import http.client
import requests

from django.conf import settings
from django.contrib.auth import authenticate, login

# Create your views here.


def send_otp(mobile , otp):
    

    url = "https://www.fast2sms.com/dev/bulkV2"
    authkey = settings.AUTH_KEY

    
    querystring = {"authorization":authkey,"variables_values":otp,"route":"otp","numbers":mobile}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    



# def login_attempt(request):
#     if request.method == 'POST':
#         mobile = request.POST.get('mobile')
        
#         user = Profile.objects.filter(mobile = mobile).first()
        
#         if user is None:
#             context = {'message' : 'User not found' , 'class' : 'danger' }
#             return render(request,'cart/login.html' , context)
        
#         otp = str(random.randint(1000 , 9999))
#         user.otp = otp
#         user.save()
#         send_otp(mobile , otp)
#         request.session['mobile'] = mobile
#         return redirect('login_otp')        
#     return render(request,'cart/login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = Profile.objects.filter(mobile=mobile).first()
        
        if otp == user.otp:
            
            
            return redirect('cart')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'cart/login_otp.html' , context)
    
    return render(request,'cart/login_otp.html' , context)
    
    

def register(request):
    if request.method == 'POST':
        
        mobile = request.POST.get('mobile')
        
        
        check_profile = Profile.objects.filter(mobile = mobile).first()
        
        if check_profile:
            if request.method == 'POST':
                mobile = request.POST.get('mobile')
                
                user = Profile.objects.filter(mobile = mobile).first()
                
                
                
                otp = str(random.randint(1000 , 9999))
                user.otp = otp
                user.save()
                send_otp(mobile , otp)
                request.session['mobile'] = mobile
                return redirect('login_otp')
            return redirect('cart')      
            
        else:
            otp = str(random.randint(1000 , 9999))
            profile = Profile( mobile=mobile , otp = otp) 
            profile.save()
            send_otp(mobile, otp)
            request.session['mobile'] = mobile
            return redirect('otp')
    return render(request,'cart/register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            return redirect('login')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'account/otp.html' , context)
            
        
    return render(request,'cart/otp.html' , context)

def index(request):
    return HttpResponse(request,"cart/cart.html")