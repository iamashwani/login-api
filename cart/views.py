from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User, Wallet
from .serializers import ProfileSerializer,VerifyOTPSerializer,UserProfileChangeSerializer,walletserializer
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
import http.client

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
                wallet = 10
                wall = Wallet.objects.create(user=instance,total_amount=wallet)
                send_otp(mobile, otp)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request,id):
        serializer = VerifyOTPSerializer(data=request.data)
        otp_sent = request.data['otp']
        mobile = request.data['mobile']
        user_id = User.objects.get(id=id)
        if otp_sent:
            old = User.objects.filter(id=user_id.id)
            if old is not None:
                old = old.first()
                otp = old.otp
                # old = User.objects.filter(id=user_mobile.id).update(otp = otp_sent)
                if User.objects.filter(id=user_id.id).update(otp = otp_sent):

                    return Response({'status': True,'detail': 'OTP is correct'})
                else:
                    return Response({'status': False,'detail': 'OTP incorrect, please try again'})

@api_view(['GET'])
def Get_Profile(request,pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserProfileChangeSerializer(snippet)
        return Response(serializer.data)


@api_view(['GET','PUT'])
def Update_Profile(request,pk):
    snippet = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserProfileChangeSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileChangeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])

def get_wallet(request, pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        return Response(serializer.data, status=200)
    
    return Response({"Something went wrong. Please try again later."}, status=404)

# @api_view(['GET','PUT'])   
# def add_money(request,pk):
#     qs = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = walletserializer(qs)
#         qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
#         qs.save()
#         return Response(serializer.data, status=200)
class addmoneyViewSet(APIView):
    serializer_class = walletserializer
    permission_classes = (AllowAny,)
    http_method_names = ['get',]
    def queryset(self,pk):
        # task_pk = dailyaskist(self.category)
        # return Task.objects.filter(pk=task_pk)
        get_queryset = Wallet.objects.filter(pk=pk)
        serializer = walletserializer(self.get_queryset)
        get_queryset.total_amount = get_queryset.total_amount + get_queryset.add_amount + get_queryset.win_amount
        get_queryset.save()
        return Response(serializer.data, status=200)



@api_view(['GET','PUT'])   
def deduct_amount(request,pk):
    qs = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = walletserializer(qs)
        if qs.add_amount > qs.deduct_amount:
            qs.add_amount = qs.add_amount - qs.deduct_amount
            qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
            qs.save()
        elif qs.win_amount > qs.deduct_amount:
            qs.win_amount = qs.win_amount - qs.deduct_amount
            qs.total_amount = qs.total_amount + qs.add_amount + qs.win_amount
            qs.save()
        else:
            return Response({status : "Not have enough balance"})

        return Response(serializer.data, status=200)
