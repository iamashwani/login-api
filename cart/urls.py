from .views import *
from django.urls import path,include
from .views import RegistrationAPIView,VerifyOTPView,UserProfileChangeAPIView
from . import views
# from rest_framework import routers
# from myapp.views import registratio




urlpatterns = [

    # path('' , login_attempt , name="login"),
    # path('register/' , register , name="register"),
    path('register/', RegistrationAPIView.as_view()),
    path('verify/', VerifyOTPView.as_view()),
    #path('update_profile/<int:id>/',views.update_profile, name='auth_update_profile'),
    path('update_profile/<int:id>/',UserProfileChangeAPIView.as_view(), name='auth_update_profile')
    # path('otp' , otp , name="otp"),
    # path('login-otp', login_otp , name="login_otp"),
    # path('cart', index , name="cart"), 
   
    
]

