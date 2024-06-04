
import datetime
from shutil import move
from rest_framework.response import Response

from rest_framework import views

from bus_routing.models import Bus, BusStation, MovementHistory, OnBusData, Ticket
from bus_routing.serializer import BusStationSerializer, MovementHistorySerializer, OnBusDataSerializer

class GetOnBusView(views.APIView):
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        end_bus_station_id = request.data.get('end_bus_station_id')
        start_bus_station_id = request.data.get('start_bus_station_id')
        try:
            on_bus_data = OnBusData.objects.get(ticket_id=ticket_id)
            return Response(status=400,data= {"status" : 400, 'message': 'this user is on bus'})
        except:
            bus_id = Ticket.objects.filter(ticket_id=ticket_id).first().bus_id
            if bus_id:
                bus = Bus.objects.get(bus_id=bus_id)
                bus.current_passenger_amount += 1
                bus.save()

            data = {
                'ticket_id': ticket_id,
                'end_bus_station_id': end_bus_station_id,
                'start_bus_station_id': start_bus_station_id
            }
            movement_history_data = {
                'ticket_id': ticket_id,
                'bus_id': Ticket.objects.get(ticket_id=ticket_id).bus_id,
                'user_id': Ticket.objects.get(ticket_id=ticket_id).user_id,
                'on_bus_at': datetime.datetime.now()
            }
            serializer = OnBusDataSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                movement_history = MovementHistory.objects.filter(ticket_id=ticket_id)
                if not movement_history:
                    movement_history_serializer = MovementHistorySerializer(data=movement_history_data)
                    if movement_history_serializer.is_valid():
                        movement_history_serializer.save()
                    else:
                        print(movement_history_serializer.errors)
                        return Response(status=400,data= {"status" : 400, 'message': 'Get on bus failed'})
                
                return Response(status=200,data= {"status" : 200, 'message': 'Get on bus successfully'})
            else:
                print(serializer.errors)
                return Response(status=400,data= {"status" : 400, 'message': 'Get on bus failed'})
            
class GetOffBusView(views.APIView):
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response(status=400,data= {"status" : 400, 'message': 'ticket_id is required'})
        try:
            on_bus_data = OnBusData.objects.get(ticket_id=ticket_id)
            on_bus_data.delete()
            bus_id = Ticket.objects.get(ticket_id=ticket_id).bus_id
            bus = Bus.objects.get(bus_id=bus_id)
            bus.current_passenger_amount -= 1
            bus.save()
            movement_history = MovementHistory.objects.get(ticket_id=ticket_id)
            movement_history.off_bus_at = datetime.datetime.now()
            movement_history.save()
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