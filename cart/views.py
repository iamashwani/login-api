from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from .models import User,Wallet,Transcations
from .serializers import ProfileSerializer, \
    VerifyOTPSerializer, UserProfileChangeSerializer,\
    GetTotalwalletserializer,UserGetProfileChangeSerializer,walletserializer_deduct,\
    walletserializer_add,GetResponceSerializer,TranscationHistoryserializer,Transcationserializer,Getreferralserializer
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
import http.client
from django.http import HttpResponse, JsonResponse
import urllib.request as urllib2


def send_otp(mobile, otp):

    authkey = settings.AUTH_KEY
    url = "http://amazesms.in/api/pushsms?user=hogotp&authkey="+authkey+"&sender=AMTSHR&mobile="+mobile+"&text=Hi%20%2C%20Your%20OTP%20is%20"+otp+".%20Valid%20for%203min.%20AMTSHR&entityid=1201159141994639834&templateid=1507164906024124641&rpt=1"

    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    data = page.read()
    print(data.decode("utf-8"))


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    def post(self, request):
        try:

            mobile = request.data['mobile']
            data = User.objects.filter(mobile=mobile).first()
            if data is not None:
                serializer = self.serializer_class(data=request.data)
                mobile = request.data['mobile']
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    content = {'status': True, 'message': 'success', 'id': instance.id,'mobile': instance.mobile, 'otp': instance.otp, 'name': instance.name,
                               'username': instance.username, 'profile_id': instance.profile_id}
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
                               'username': instance.username,'profile_id': instance.profile_id}
                    mobile = instance.mobile
                    otp = instance.otp
                    wallet = 10
                    wall = Wallet.objects.create(user=instance,total_amount=wallet)
                    send_otp(mobile, otp)
                    return JsonResponse(content, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'status': False, "message": "Login in Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request, id):
        try:
            serializer = VerifyOTPSerializer(data=request.data)
            otp_sent = request.data['otp']
            otp = User.objects.get(pk=id)
            if otp_sent:
                old = User.objects.filter(id=otp.id)
                if old is not None:
                    old = old.first()
                    otp = old.otp
                    if str(otp) == str(otp_sent):
                        return JsonResponse({'status': True,'message': 'OTP is correct'})
                    else:
                        return JsonResponse({'status': False,'message': 'OTP incorrect, please try again'})
        except:
            return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def Get_Profile(request, pk):
    try:
        if request.method == 'GET':
            snippet = User.objects.get(pk=pk)
            serializer = UserGetProfileChangeSerializer(snippet)
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET', 'POST'])
def Update_Profile(request,pk):
    try:
        if request.method == 'GET':
            snippet = User.objects.get(pk=pk)
            serializer = UserProfileChangeSerializer(snippet)
            return Response(serializer.data)
        elif request.method == 'POST':
            snippet = User.objects.get(pk=pk)
            serializer = UserProfileChangeSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                json_data = serializer.data
                x = GetResponceSerializer(json_data)
                x = {**x.data, **json_data}
                return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def get_wallet(request, pk):
    try:
        qs = Wallet.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = GetTotalwalletserializer(qs)
            qs.total_amount = qs.total_amount + qs.winning_cash
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse({"status": False, "message": "Something went wrong. Please try again later."}, status=404)
    except:
        return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET', 'POST'])
def transcationmoney(request, pk):
    if request.method == 'POST':

        user = User.objects.get(pk=pk)
        qs = Wallet.objects.get(pk=pk)
        serializer = Transcationserializer(qs, data=request.data)
        if serializer.is_valid(raise_exception=True):
            amount = request.data['amount']
            qs.amount = amount
            description = request.data['description']
            if amount > 0:
                qs.winning_cash = qs.winning_cash + amount
                qs.save()
            elif amount < 0:
                qs.winning_cash = qs.winning_cash + amount
                qs.save()
            obj = Transcations.objects.create(user=user,wallet=qs, amount=qs.amount,description=description,winning_cash=qs.winning_cash)
            obj.save()
        json_data = serializer.data
        x = GetResponceSerializer(json_data)
        x = {**x.data, **json_data}
        return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later", },
                            status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def TranscationsHistory(request,pk):
    if request.method == 'GET':
        wll = Wallet.objects.get(pk=pk)
        qs = Transcations.objects.filter(wallet=wll).order_by('-pk')
        serializer = TranscationHistoryserializer(qs)
        json_data = []
        for x in qs:
            json_data.append({
                'id': x.pk,
                'amount': x.amount,
                'description': x.description,
                'date': x.insert_date_and_time,
            })
        return JsonResponse({"status": True, "message": "success", "data": json_data}, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getreferral(request, pk):
    try:
        qs = Wallet.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = Getreferralserializer(qs)
            json_data = serializer.data
            x = GetResponceSerializer(json_data)
            x = {**x.data, **json_data}
            return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(json_data,status=status.HTTP_200_OK, safe=False)
    except:
        return JsonResponse({"status": False, "message": "Something went wrong. Please try again later"}, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework import viewsets
# class SpeciesViewSet(viewsets.ModelViewSet):
#    queryset = Transcations.objects.all()
#    serializer_class = Transcations

# @api_view(['GET'])
# def total_of_add_money(request,pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer(qs)
#             qs.total_amount = qs.total_amount + qs.add_amount
#             qs.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response('')
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                             status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
# @api_view(['GET'])
# def total_of_win_money(request,pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer(qs)
#             qs.total_amount = qs.total_amount + qs.win_amount
#             qs.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response('')
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                             status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#
#
# @api_view(['GET'])
# def full_money(request, pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer_add(qs)
#             qs.deposit_cash = qs.deposit_cash + qs.add_amount
#             qs.winning_cash = qs.winning_cash + qs.win_amount
#             qs.save()
#             json_data = serializer.data
#             x = GetResponceSerializer(json_data)
#             x = {**x.data, **json_data}
#             return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
#         else:
#             return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                         status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#
# @api_view(['GET'])
# def withdraw_amount(request, pk):
#     try:
#         qs = Wallet.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = walletserializer_deduct(qs)
#             if qs.winning_cash > qs.withdraw_amount:
#                 qs.winning_cash = qs.winning_cash - qs.withdraw_amount
#                 qs.total_amount = qs.total_amount - qs.withdraw_amount
#                 qs.save()
#                 json_data = serializer.data
#                 x = GetResponceSerializer(json_data)
#                 x = {**x.data, **json_data}
#                 return JsonResponse(x, status=status.HTTP_200_OK, safe=False)
#             else:
#                 return JsonResponse({"status": False, "message": "Something went wrong. Please try again later",}, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },
#                         status=status.HTTP_503_SERVICE_UNAVAILABLE)