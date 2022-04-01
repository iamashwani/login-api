from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User
from .serializers import ProfileSerializer, VerifyOTPSerializer,UserProfileChangeSerializer
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
import requests
from rest_framework import generics, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
def send_otp(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    authkey = settings.AUTH_KEY
    querystring = {"authorization": authkey, "variables_values": otp, "route": "otp", "numbers": mobile}
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
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            mobile = request.data['mobile']
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                content = {'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                           'username': instance.username, 'logo': instance.logo, 'profile_id': instance.profile_id}
                mobile = instance.mobile
                otp = instance.otp
                send_otp(mobile, otp)
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

                    return Response({
                        'status': True,
                        'detail': 'OTP is correct'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })

class UserProfileChangeAPIView(APIView):
    # permission_classes = (AllowAny,)
    # queryset=User.objects.all()
    serializer_class = UserProfileChangeSerializer
    # parser_classes = (MultiPartParser, FormParser,)
    def get(self, request,id):
        # import pdb
        # pdb.set_trace()
    
        serializer = UserProfileChangeSerializer(data=request.data)
        userProfileObj = User.objects.filter(id=id)
        if serializer.is_valid():
            serializer.save()

        return Response(userProfileObj,serializer.data)

    # def put(self,request,id):
    #     serializer = UserProfileChangeSerializer(data=request.data)
    #     id = request.data['id']        # serializer = UserProfileChangeSerializer(blog_post, data=request.data)
    
    #     if serializer.is_valid():
    #         serializer.save()
                
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT',])
# def api_update_blog_view(request, id):

# 	try:
# 		blog_post = User.objects.get(id = id)
# 	except User.DoesNotExist:
# 		return Response(status=status.HTTP_404_NOT_FOUND)

# 	if request.method == 'PUT':
# 		serializer = UserProfileChangeSerializer(blog_post, data=request.data)
# 		data = {}
# 		if serializer.is_valid():
# 			serializer.save()
			
# 			return Response(data=data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET','PUT'])
# def update_profile(request):
#     if request.method == 'GET':
#         user  = User.objects.get(id=request.user.id)
#         serializer_user = UserProfileChangeSerializer(user, many=True)
        
#         result = {'serializer_user': serializer_user.data}
#         return Response(result)
#     elif request.method == 'PUT':
#         user  = User.objects.get(id=request.user.id)
      
#         serializer_user = UserProfileChangeSerializer(user, data=request.data)
        
#         if serializer_user.is_valid():
#             serializer_user.save()
            
#             result = {'serializer_user': serializer_user.data}
#             return Response(result)
#         result = {'serializer_user': serializer_user.data}
#         return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)