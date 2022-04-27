from django.shortcuts import render
from rest_framework.decorators import APIView
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from cart.models import User
# Create your views here.

@api_view(['GET','POST'])
def TicketViewSet(request, id):
    try:
        import pdb
        pdb.set_trace()
        user = User.objects.get(id=id)
        if request.method == 'POST':
            # user = User.objects.get(id=id)
            
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                title = request.data['title']
               
                content = request.data['content']
                
                status1  = request.data['status1']
                
                qs = Ticket.objects.create(title=title,content = content,status1 = status1,user = user)
                qs.save()
                return Response(serializer.data,{'status': True,'message': 'Filled Successfully'},status=status.HTTP_200_OK,safe=False)
            else:
                return JsonResponse({'status': False,'message': 'Ni ho rha'})
    except:
            return JsonResponse({"status": False, "message": "Service temporarily unavailable, try again later", },status=status.HTTP_503_SERVICE_UNAVAILABLE)