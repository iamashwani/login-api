from .views import *
from django.urls import path,include
from .views import RegistrationAPIView,VerifyOTPView
from . import views
urlpatterns = [

    path('register/', RegistrationAPIView.as_view()),
    path('verify/<int:id>', VerifyOTPView.as_view()),
    path('get_profile/<int:pk>',views.Get_Profile, name='get_profile'),
    path('update_profile/<int:pk>',views.Update_Profile, name='update_profile'),

    path('get_wallet/<int:pk>',views.get_wallet, name='get_wallet'),
    path('total_of_add_money/<int:pk>',views.total_of_add_money, name='total_of_add_money'),
    path('total_of_win_money/<int:pk>',views.total_of_win_money, name='total_of_win_money'),

    path('full_money/<int:pk>',views.full_money, name='full_add_money'),
    #path('full_win_money/<int:pk>',views.full_win_money, name='full_win_money'),
    path('withdraw_amount/<int:pk>',views.withdraw_amount, name='withdraw_amount')    
]

