from rest_framework import serializers
from bus_routing.models import Bus, BusRouting, BusStation, Deposit, MovementHistory, OnBusData, Ticket, TicketStation
from django.contrib.auth.models import User


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('user_id', 'amount')

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('bus_number', 'driver_name', 'current_passenger_amount', 'max_passenger_amount', 'speed')

class OnBusDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnBusData
        fields = ('ticket_id', 'end_bus_station_id', 'start_bus_station_id')

class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = ('bus_station_id', 'name', 'latitude', 'longitude', 'bus_number')


class BusRoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRouting
        fields = ('bus_number', 'bus_station')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'user_id', 'bus_number', 'status', 'price', 'valid_to', 'bus_id')   

class TicketStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStation
        fields = ('ticket_id', 'bus_number', 'on_bus_station_id', 'off_bus_station_id')

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class MovementHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementHistory
        fields = ('ticket_id','bus_id', 'user_id', 'on_bus_at', 'off_bus_at')
