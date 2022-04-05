from .views import *
from django.urls import path,include
from .views import RegistrationAPIView,VerifyOTPView
from . import views





urlpatterns = [

    path('register/', RegistrationAPIView.as_view()),
    path('verify/<int:pk>', VerifyOTPView.as_view()),
    path('get_profile/<int:pk>',views.Get_Profile, name='get_profile'),
    path('update_profile/<int:pk>',views.Update_Profile, name='update_profile'),
    path('get_wallet/<int:pk>',views.get_wallet, name='get_wallet'),
    #path('add_money/<int:pk>',views.add_money, name='add_money'),

    
]

