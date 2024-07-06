
from django.contrib import admin
from django.urls import path

from bus_routing.api.bus import BusView, GetBusIdView, GetBusInfomationByBusNumberView, GetBusInfomationByIdView, GetBusNumberView, UpdateCurrentPassengerAmountView
from bus_routing.api.feedback import feedbackView
from bus_routing.api.hello import BusStationHelloView
from bus_routing.api.mail import RequestOTPView, VerifyOTPView
from bus_routing.api.momo import MomoStatusView, MomoView
from bus_routing.api.passenger import PassengerDataView
from bus_routing.api.payment import BuyTicketView, DepositView
from bus_routing.api.station import BusStationView, FindBusStationByNameView, GetBusStationByBusNumberView, GetBusStationByNameView, GetBusStationIdView, GetOffBusView, GetOnBusView, GetStationByBusNumber, GetUpcomingBusInfomationView
from bus_routing.api.ticket import CheckTicketView, GetUserTicket
from bus_routing.api.users import UserDetailView

urlpatterns = [
    path('deposit', DepositView.as_view()),
    path('buy_ticket', BuyTicketView.as_view()),
    path('current_passenger_amount', BusView.as_view()),
    path('get_on_bus', GetOnBusView.as_view()),
    path('get_off_bus', GetOffBusView.as_view()),

    # path('add_bus_station', BusStationView.as_view()),
    path('get_station_by_bus_number', GetStationByBusNumber.as_view()),
    path('get_all_bus_station', BusStationView.as_view()),
    path('get_bus_station_by_name', GetBusStationByNameView.as_view()),
    path('get_bus_station_by_bus_number', GetBusStationByBusNumberView.as_view()),
    path('get_upcoming_bus_information', GetUpcomingBusInfomationView.as_view()),
    path('find_bus_station_by_name', FindBusStationByNameView.as_view()),

    path('add_bus_information', BusView.as_view()),
    path('get_bus_id', GetBusIdView.as_view()),
    path('get_bus_information_by_id', GetBusInfomationByIdView.as_view()),
    path('get_bus_info_by_bus_number', GetBusInfomationByBusNumberView.as_view()),
    path('get_list_bus_bus_number', GetBusNumberView.as_view()),
    path('update_current_passenger_amount', UpdateCurrentPassengerAmountView.as_view()),

    path('get_station_id', GetBusStationIdView.as_view()),
    path('save_ticket_information', BuyTicketView.as_view()),
    path('update_ticket_information', BuyTicketView.as_view()),
    path('check_ticket', CheckTicketView.as_view()),
    path('request-otp', RequestOTPView.as_view(), name='request_otp'),
    path('verify-otp', VerifyOTPView.as_view(), name='verify_otp'),
    path('user', UserDetailView.as_view(), name='user-detail'),
    path('user_tickets', GetUserTicket.as_view(), name='user-tickets'),

    path('momo', MomoView.as_view()),
    path('momo_status', MomoStatusView.as_view()),

    path('feedback', feedbackView.as_view()),
    
    path('get_passenger_data/<str:period>/<str:interval>/', PassengerDataView.as_view()),
]


