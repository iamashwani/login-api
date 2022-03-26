# from .views import *
from django.urls import path
from .views import DepositAmount


urlpatterns = [
    path('wallet/', DepositAmount.as_view()),

]
