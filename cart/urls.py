from .views import *
from django.urls import path, include
from .views import RegistrationAPIView, VerifyOTPView
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    path('register/', RegistrationAPIView.as_view()),
    path('verify/', VerifyOTPView.as_view()),
    path('get_profile/<int:pk>/', views.Get_Profile, name='get_profile'),
    path('update_profile/<int:pk>', views.Update_Profile, name='update_profile'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('get_wallet/<int:pk>', views.get_wallet, name='get_wallet'),
    # path('add_money/<int:pk>', views.add_money, name='add_money'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
