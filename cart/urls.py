from .views import *
from django.urls import path
from .views import RegistrationAPIView,VerifyOTPView


urlpatterns = [
    path('api/vi/register/', RegistrationAPIView.as_view()),
    path('api/vi/verify/', VerifyOTPView.as_view()),

   
    
]

