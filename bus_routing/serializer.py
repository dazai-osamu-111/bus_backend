from rest_framework import serializers
from bus_routing.models import Bus, BusRouting, BusStation, Deposit, OnBusData


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