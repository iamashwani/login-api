from .views import *
from django.urls import path,include
from .views import RegistrationAPIView,VerifyOTPView,addmoneyViewSet
from . import views
urlpatterns = [

    path('register/', RegistrationAPIView.as_view()),
    path('verify/<int:id>', VerifyOTPView.as_view()),
    path('get_profile/<int:pk>',views.Get_Profile, name='get_profile'),
    path('update_profile/<int:pk>',views.Update_Profile, name='update_profile'),
    path('get_wallet/<int:pk>',views.get_wallet, name='get_wallet'),
    # path('add_money/<int:pk>',views.add_money, name='add_money'),
    path('add_money/<int:pk>',addmoneyViewSet.as_view()),
    path('deduct_amount/<int:pk>',views.deduct_amount, name='deduct_amount')    
]

