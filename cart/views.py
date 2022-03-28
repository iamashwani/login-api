from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User
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
        data = User.objects.filter(mobile = mobile).first()
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

        if mobile and otp_sent:
            old = User.objects.filter(mobile=mobile)
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


