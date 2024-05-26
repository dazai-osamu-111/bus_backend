
from django.contrib import admin
from django.urls import path

from bus_routing.api.hello import BusStationHelloView
from bus_routing.api.payment import DepositView

urlpatterns = [
    path('deposit', DepositView.as_view()),
]


