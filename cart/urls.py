from django.urls import path, include
from .views import RegistrationAPIView, VerifyOTPView
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    path('register/', RegistrationAPIView.as_view()),
    path('verify/<int:id>/', VerifyOTPView.as_view()),

    path('get_profile/<int:pk>/', views.Get_Profile, name='get_profile'),
    path('update_profile/<int:pk>/', views.Update_Profile, name='update_profile'),

    path('get_wallet/<int:pk>/', views.get_wallet, name='get_wallet'),
    path('transaction/<int:pk>/', views.transactionmoney, name='transaction'),
    path('transaction_history/<int:pk>/', views.transactionsHistory, name='transaction_history'),

    path('getreferral/<int:pk>/', views.getreferral, name='getreferral'),
    path('redeem_referral_code/<int:pk>/', views.RedeemReferralcode, name='redeem_referral_code'),

    path('get_bonus_money/<int:pk>/', views.get_bonus_money, name='get_bonus_money'),

    path('bonus_money/<int:pk>/', views.bonus_money, name='bonus_money')

    # path('referral/', RefferCodeJsonView.as_view()),

    # path('total_of_add_money/<int:pk>', views.total_of_add_money, name='total_of_add_money'),
    # path('total_of_win_money/<int:pk>', views.total_of_win_money, name='total_of_win_money'),
    # path('full_money/<int:pk>/', views.full_money, name='full_money'),
    # path('withdraw_amount/<int:pk>/', views.withdraw_amount, name='withdraw_amount'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)

# handler404 = 'cart.views.api_500_handler'
