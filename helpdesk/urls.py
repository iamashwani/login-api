from django.urls import path
from .views import TicketViewSet
from . import views


urlpatterns = [
    path('TicketViewSet/<int:id>', views.TicketViewSet,name = "TicketViewSet"),
]