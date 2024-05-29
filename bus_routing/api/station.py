from tracemalloc import start
from rest_framework.response import Response

from rest_framework import views

from bus_routing.models import BusStation, OnBusData
from bus_routing.serializer import BusStationSerializer, OnBusDataSerializer

class GetOnBusView(views.APIView):
    def post(self, request):
        bus_id = request.data.get('bus_id')
        user_id = request.data.get('user_id')
        end_bus_station_id = request.data.get('end_bus_station_id')
        start_bus_station_id = request.data.get('start_bus_station_id')
        try:
            on_bus_data = OnBusData.objects.get(bus_id=bus_id, user_id=user_id)
            return Response(status=400,data= {"status" : 400, 'message': 'this user is on bus'})
        except:  
            
            data = {
                'bus_id': bus_id,
                'user_id': user_id,
                'end_bus_station_id': end_bus_station_id,
                'start_bus_station_id': start_bus_station_id
            }
            serializer = OnBusDataSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200,data= {"status" : 200, 'message': 'Get on bus successfully'})
            else:
                print(serializer.errors)
                return Response(status=400,data= {"status" : 400, 'message': 'Get on bus failed'})
            
class GetOffBusView(views.APIView):
    def post(self, request):
        bus_id = request.data.get('bus_id')
        user_id = request.data.get('user_id')
        if not bus_id or not user_id:
            return Response(status=400,data= {"status" : 400, 'message': 'bus_id, user_id are required'})
        try:
            on_bus_data = OnBusData.objects.get(bus_id=bus_id, user_id=user_id)
            on_bus_data.delete()
            return Response(status=200,data= {"status" : 200, 'message': 'Get off bus successfully'})
        except:  
            return Response(status=400,data= {"status" : 400, 'message': 'this user is not on bus'})
class BusStationView(views.APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if  not name or not latitude or not longitude:
            return Response({"status" : 400, 'message': 'bus_station_id, name, latitude, longitude are required'})
        try:
            bus_station = BusStation.objects.get(name=name)
            return Response({"status" : 400, 'message': 'bus station is existed'})
        except: 
            data = {
                'name': name,
                'latitude': latitude,
                'longitude': longitude
            }
            serializer = BusStationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status" : 200, 'message': 'add bus station successfully'})
            else:
                return Response({"status" : 400, 'message': 'addd bus station failed'})
            

class GetBusStationIdView(views.APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"status" : 400, 'message': 'param name is required'})
        try:
            bus_station = BusStation.objects.get(name=name)
            return Response({"status" : 200, 'bus_station_id': bus_station.bus_station_id})
        except:
            return Response({"status" : 400, 'message': 'bus station not found'})