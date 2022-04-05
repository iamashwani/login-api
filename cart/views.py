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
from django.db import transaction
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
                send_otp(mobile, otp)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request,id):
        serializer = VerifyOTPSerializer(data=request.data)
        #mobile = request.data['mobile']
        otp_sent = request.data['otp']
        otp = User.objects.get(pk = id)
        if otp_sent:
            
            old = User.objects.filter(id=otp.id)
            if old is not None:
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):

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

# @api_view(['GET'])
# def get_wallet(request,pk):
#     snippet = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = walletserializer(snippet)
#         return Response(serializer.data)

# class BalanceView(APIView):
#     allowed_methods = ['get', 'post']
#     serializer_class = walletserializer
    
#     def get_queryset(self):
#         return Wallet.objects.filter(pk=self.request.user)
    
#     def post(self, request, *args, **kwargs):
#         serializer = walletserializer(data = request.data)
#         if serializer.is_valid(raise_exception = True):
#             serializer.save()
#             with transaction.atomic():
#                 Wallet.objects.filter(pk=self.request.user).update(total_amount = f'total_amount' + serializer.validated_data.get('total_amount', 0))
#                 return Response({"message":'money added successfully'}, status = status.HTTP_201_CREATED)
#         return Response({status: status.HTTP_400_BAD_REQUEST})
    
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
#         return Response(serializer.data, status=200)
        
#     elif request.method == 'PUT':
#         amount_to_deposit = float(request.data.get("amount"))
#         if amount_to_deposit < 0.0 :
#             return Response({"Amount invalid!"}, status=400)
#         qs = Wallet.objects.get(pk=pk)
#         serializer = walletserializer(qs)
#         qs.total_amount = qs.total_amount + amount_to_deposit
#         qs.save()
#         return Response({"Deposit successful."}, status=200)
    
#     return Response({"Something went wrong. Please try again later."}, status=404)


# from cart.models import Wallet  
# wallet = User.wallet_set.create()

# with transaction.atomic():
#     # We need to lock the wallet first so that we're sure
#     # that nobody modifies the wallet at the same time 
#     # we're modifying it.
#     wallet = Wallet.select_for_update().get(pk=wallet.id)
#     wallet.deposit(100)  # amount
    
    
# with transaction.atomic():
#     # We need to lock the wallet first so that we're sure
#     # that nobody modifies the wallet at the same time 
#     # we're modifying it.
#     wallet = Wallet.select_for_update().get(pk=wallet.id)
#     wallet.withdraw(100)  

# # @api_view(['GET','PUT'])
# # def update_profile(request,pk):
# #     snippet = Wallet.objects.get(pk=pk)
# #     if request.method == 'GET':
# #         serializer = walletserializer(snippet)
# #         return Response(serializer.data)
    
# #     elif request.method == 'PUT':
# #         serializer = walletserializer(snippet, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             total_amount = request.data['total_amount']
# #             add_amount = request.data['add_amount']
# #             win_amount = request.data['win_amount']
# #             deduct_amount = request.data['deduct_amount']
# #             if add_amount > 0 or win_amount > 0:
# #                 total_amount = add_amount + win_amount
                
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
