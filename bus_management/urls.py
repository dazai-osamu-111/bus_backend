
from django.contrib import admin
from django.urls import path

from bus_routing.api.bus import BusView
from bus_routing.api.hello import BusStationHelloView
from bus_routing.api.payment import BuyTicketView, DepositView
from bus_routing.api.station import BusStationView, GetOffBusView, GetOnBusView

urlpatterns = [
    path('deposit', DepositView.as_view()),
    path('buy_ticket', BuyTicketView.as_view()),
    path('current_passenger_amount', BusView.as_view()),
    path('get_on_bus', GetOnBusView.as_view()),
    path('get_off_bus', GetOffBusView.as_view()),
    path('add_bus_station', BusStationView.as_view()),
    path('add_bus_information', BusView.as_view()),
    # path('add_bus_routing',)
]


