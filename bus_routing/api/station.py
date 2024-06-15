
from datetime import datetime

import googlemaps
from rest_framework.response import Response

from rest_framework import views

from bus_routing.models import Bus, BusStation, MovementHistory, OnBusData, Ticket, TicketStation
from bus_routing.serializer import BusStationSerializer, MovementHistorySerializer, OnBusDataSerializer

class GetOnBusView(views.APIView):
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        bus_id = request.data.get('bus_id')
        on_bus_data = OnBusData.objects.filter(ticket_id=ticket_id).first()
        if on_bus_data:
            return Response(status=400,data= {"status" : 400, 'message': 'this user is on bus'})
        ticket = Ticket.objects.filter(ticket_id=ticket_id).first()
        if not ticket:
            return Response(status=400,data= {"status" : 400, 'message': 'this ticket is not valid'})
        ticket.bus_id = bus_id
        ticket.save()
        bus = Bus.objects.get(bus_id=bus_id)
        bus.current_passenger_amount += 1
        bus.save()

        bus_number = bus.bus_number
        ticket_station = TicketStation.objects.filter(ticket_id=ticket_id, bus_number=bus_number).first()
        if not ticket_station:
            return Response(status=400,data= {"status" : 400, 'message': 'this ticket is not valid'})
        start_bus_station_id = ticket_station.on_bus_station_id
        end_bus_station_id = ticket_station.off_bus_station_id


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
            
            movement_history = MovementHistory.objects.filter(ticket_id=ticket_id, bus_id=bus_id)
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
        bus_station_id = request.data.get('bus_station_id')
        bus_id = request.data.get('bus_id')
        count = 0
        if not bus_station_id or not bus_id:
            return Response(status=400,data= {"status" : 400, 'message': 'bus_station_id, bus_id is required'})
        try:
            ticket_list = Ticket.objects.filter(status=0, bus_id=bus_id)
            if not ticket_list:
                return Response(status=400,data= {"status" : 400, 'message': 'this bus is empty'})
            ticket_list = list(ticket_list)
            bus_number = Bus.objects.filter(bus_id=bus_id).first().bus_number
            if not bus_number:
                return Response(status=400,data= {"status" : 400, 'message': 'bus number not found'})
            for ticket in ticket_list:
                ticket_id = ticket.ticket_id
                off_bus_station_id = TicketStation.objects.filter(ticket_id=ticket_id, bus_number=bus_number).last().off_bus_station_id
                if off_bus_station_id:
                    if off_bus_station_id == bus_station_id:
                        on_bus_data = OnBusData.objects.get(ticket_id=ticket_id)
                        on_bus_data.delete()
                        bus_id = Ticket.objects.get(ticket_id=ticket_id).bus_id
                        bus = Bus.objects.get(bus_id=bus_id)
                        bus.current_passenger_amount -= 1
                        bus.save()
                        last_ticket_station = TicketStation.objects.filter(ticket_id=ticket_id).last()
                        if last_ticket_station:
                            last_ticket_station_id = last_ticket_station.off_bus_station_id
                            if last_ticket_station_id == bus_station_id:
                                ticket = Ticket.objects.get(ticket_id=ticket_id)
                                ticket.status = 1
                                ticket.save()
                        movement_history = MovementHistory.objects.filter(ticket_id=ticket_id, bus_id=bus_id).first()
                        movement_history.off_bus_at = datetime.datetime.now()
                        movement_history.save()
                        count+=1
            if count == 0:
                return Response(status=400,data= {"status" : 400, 'message': 'get of 0 passenser'})
            else:
                return Response(status=200,data= {"status" : 200, 'message': 'Get off bus successfully'})
        except:  
            return Response(status=400,data= {"status" : 400, 'message': 'this user is not on bus'})
class BusStationView(views.APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        bus_number = data.get('bus_number')
        if  not name or not latitude or not longitude or not bus_number:
            return Response({"status" : 400, 'message': 'bus_number, name, latitude, longitude are required'})
        try:
            bus_station = BusStation.objects.get(name=name, bus_number=bus_number)
            return Response({"status" : 400, 'message': 'bus station is existed'})
        except: 
            data = {
                'name': name,
                'latitude': latitude,
                'longitude': longitude,
                'bus_number': bus_number
            }
            
            serializer = BusStationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status" : 200, 'message': 'add bus station successfully'})
            else:
                return Response({"status" : 400, 'message': 'addd bus station failed'})
            
    def get(self, request):
        bus_station = BusStation.objects.all()
        serializer = BusStationSerializer(bus_station, many=True)
        return Response({"status" : 200, 'data': serializer.data})
            

class GetBusStationIdView(views.APIView):
    def get(self, request):
        name = request.query_params.get('name')
        bus_number = request.query_params.get('bus_number')
        if not name:
            return Response({"status" : 400, 'message': 'param name is required'})
        if not bus_number:
            return Response({"status" : 400, 'message': 'param bus_number is required'})
        try:
            bus_station = BusStation.objects.filter(name=name, bus_number=bus_number).first()
            bus_station_serializer = BusStationSerializer(bus_station)
            return Response({"status" : 200, 'bus_station': bus_station_serializer.data})
        except:
            return Response({"status" : 400, 'message': 'bus station not found'})
class GetStationByBusNumber(views.APIView):
    def get(self, request):
        bus_number = request.query_params.get('bus_number')
        if not bus_number:
            return Response({"status" : 400, 'message': 'param bus_number is required'})
        bus_station = BusStation.objects.filter(bus_number=bus_number)
        serializer = BusStationSerializer(bus_station, many=True)
        return Response({"status" : 200, 'data': serializer.data})
    
class GetBusStationByNameView(views.APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"status" : 400, 'message': 'param name is required'})
        bus_station = BusStation.objects.filter(name=name)
        serializer = BusStationSerializer(bus_station, many=True)
        return Response({"status" : 200, 'data': serializer.data})
    
class GetBusStationByBusNumberView(views.APIView):
    def get(self, request):
        bus_number = request.query_params.get('bus_number')
        direction = request.query_params.get('direction')
        if not bus_number:
            return Response({"status" : 400, 'message': 'param bus_number is required'})
        if not direction:
            return Response({"status" : 400, 'message': 'param direction is required'})
        bus_station = BusStation.objects.filter(bus_number=bus_number, direction=direction)
        serializer = BusStationSerializer(bus_station, many=True)
        return Response({"status" : 200, 'data': serializer.data})
    

# API key của Google Maps
GOOGLE_MAPS_API_KEY = 'AIzaSyAnI_7dbzhe2FS7kr1lXvqXId2AIBvUXB8'

# Hàm kết nối tới Google Maps API
def get_gmaps_client(api_key):
    return googlemaps.Client(key=api_key)

class GetUpcomingBusInfomationView(views.APIView):
    def get(self, request):
        bus_station_name = request.query_params.get('bus_station_name')
        if not bus_station_name:
            return Response({"status": 400, 'message': 'param bus_station_name is required'})
        
        bus_station = BusStation.objects.filter(name=bus_station_name).first()
        if not bus_station:
            return Response({"status": 404, 'message': 'Bus station not found'})
        
        bus_longitude = bus_station.longitude
        bus_latitude = bus_station.latitude
        
        # Tách các giá trị từ bus_number_list_go và bus_number_list_return
        bus_number_list_go = bus_station.bus_number_list_go.split(",") if bus_station.bus_number_list_go else []
        bus_number_list_return = bus_station.bus_number_list_return.split(",") if bus_station.bus_number_list_return else []
        
        # Gộp lại và loại bỏ giá trị trùng lặp
        bus_number_of_bus_station = list(set(bus_number_list_go + bus_number_list_return))

        upcoming_buses_info = []

        gmaps = get_gmaps_client(GOOGLE_MAPS_API_KEY)

        for bus_number in bus_number_of_bus_station:
            bus_list = Bus.objects.filter(bus_number=bus_number)
            for bus in bus_list:
                result = gmaps.distance_matrix(
                    origins=f"{bus.current_latitude},{bus.current_longitude}",
                    destinations=f"{bus_latitude},{bus_longitude}",
                    mode="driving",
                    departure_time=datetime.now()
                )

                if result['rows'][0]['elements'][0]['status'] == 'OK':
                    distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000  # chuyển đổi sang km
                    duration = result['rows'][0]['elements'][0]['duration']['value'] / 60  # chuyển đổi sang phút

                    if distance < 5 and duration < 40:
                        bus_info = {
                            "bus_number": bus.bus_number,
                            "driver_name": bus.driver_name,
                            "current_passenger_amount": bus.current_passenger_amount,
                            "max_passenger_amount": bus.max_passenger_amount,
                            "speed": bus.speed,
                            "distance_to_station": distance,
                            "time_to_station": duration,
                            "current_latitude": bus.current_latitude,
                            "current_longitude": bus.current_longitude
                        }
                        upcoming_buses_info.append(bus_info)

        # Trả về kết quả
        return Response({"status": 200, 'upcoming_buses': upcoming_buses_info})