from rest_framework import serializers
from bus_routing.models import Bus, BusRouting, BusStation, Deposit, OnBusData, Ticket
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
        fields = ('bus_id', 'user_id', 'end_bus_station_id', 'start_bus_station_id')

class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = ('bus_station_id', 'name', 'latitude', 'longitude')


class BusRoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRouting
        fields = ('bus_number', 'bus_station')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('user_id', 'bus_number', 'status', 'price', 'valid_to')   

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']