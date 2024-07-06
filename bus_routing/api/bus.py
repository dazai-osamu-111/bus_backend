
from rest_framework.response import Response


from rest_framework import views

from bus_routing.models import Bus, OnBusData
from bus_routing.serializer import BusSerializer

class BusView(views.APIView):
    def get(self, request):
        bus_number = request.query_params.get('bus_number')
        driver_name = request.query_params.get('driver_name')
        try:
            bus = Bus.objects.get(bus_number=bus_number, driver_name=driver_name)
            speed = bus.speed
            return Response({
                'current_passenger_amount': bus.current_passenger_amount,
                'max_passenger_amount': bus.max_passenger_amount,
                'speed': speed,
                'status': 200,
            })
        except:
            return Response({"status" : 400, 'message': 'Bus not found'})

    def put(self, request):
        data = request.data
        bus_id = data.get('bus_id')
        speed = data.get('speed', 20)
        current_longitude = data.get('current_longitude', None)
        current_latitude = data.get('current_latitude', None)

        if not bus_id or not speed:
            return Response({"status" : 400, 'message': 'bus_number, driver_name, speed are required'})
        try:
            bus = Bus.objects.get(bus_id=bus_id)

            data = {
                'speed': speed,
                'current_longitude': current_longitude,
                'current_latitude': current_latitude,
            }
            serializer = BusSerializer(bus,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status" : 200, 'message': 'Update bus successfully'})
            else:
                return Response({"status" : 400, 'message': 'Update bus failed'})
        except:
            return Response({"status" : 400, 'message': 'Bus not found'})
            
class UpdateCurrentPassengerAmountView(views.APIView):
    def put(self, request):
        data = request.data
        bus_id = data.get('bus_id')
        type_update = data.get('type_update', None)
        get_off_amount = data.get('get_off_amount')
        if not bus_id or not get_off_amount:
            return Response({"status" : 400, 'message': 'bus_id, current_passenger_amount are required'})
        try:
            bus = Bus.objects.get(bus_id=bus_id)
            if type_update is not None:
                bus.current_passenger_amount = 0
            else:
                bus.current_passenger_amount -= get_off_amount
            bus.save()
            return Response({"status" : 200, 'message': 'Update current_passenger_amount successfully'})
        except:
            return Response({"status" : 400, 'message': 'Bus not found'})
class GetBusIdView(views.APIView):
    def get(self, request):
        bus_number = request.query_params.get('bus_number')
        driver_name = request.query_params.get('driver_name')
        if not bus_number or not driver_name:
            return Response({"status" : 400, 'message': 'param bus_number, driver_name are required'})
        try:
            bus = Bus.objects.get(bus_number=bus_number, driver_name=driver_name)
            return Response({
                'bus_id': bus.bus_id,
                'status': 200,
            })
        except:
            return Response({"status" : 400, 'message': 'Bus not found'})

class GetBusInfomationByBusNumberView(views.APIView):
    def get(self, request):
        bus_number = request.query_params.get('bus_number')
        if not bus_number:
            return Response({"status" : 400, 'message': 'param bus_number is required'})
        bus_data = Bus.objects.filter(bus_number__contains=bus_number)
        if not bus_data:
            return Response({"status" : 400, 'message': 'Bus not found'})
        result = []
        for bus in bus_data:
            result.append({
                'bus_id': bus.bus_id,
                'bus_number': bus.bus_number,
                'driver_name': bus.driver_name,
                'speed': bus.speed,
                'current_position': bus.current_position,
                'current_passenger_amount': bus.current_passenger_amount,
                'max_passenger_amount': bus.max_passenger_amount,
            })
        return Response({ 'status': 200, 'data': result })

class GetBusInfomationByIdView(views.APIView):
    def get(self, request):
        bus_id = request.query_params.get('bus_id')
        if not bus_id:
            return Response({"status" : 400, 'message': 'param bus_id is required'})
        try:
            bus = Bus.objects.get(bus_id=bus_id)
            return Response({
                'bus_number': bus.bus_number,
                'driver_name': bus.driver_name,
                'speed': bus.speed,
                'current_longitude': bus.current_longitude,
                'current_latitude': bus.current_latitude,
                'current_passenger_amount': bus.current_passenger_amount,
                'max_passenger_amount': bus.max_passenger_amount,
                "bus_number_name": bus.bus_number_name,
                'status': 200,
            })
        except:
            return Response({"status" : 400, 'message': 'Bus not found'})
    
class GetBusNumberView(views.APIView):
    def get(self, request):
        bus_number = request.query_params.get('bus_number')
        if not bus_number:
            return Response({"status": 400, 'message': 'param bus_number is required'})

        bus_numbers = Bus.objects.filter(bus_number__contains=bus_number).values_list('bus_number', flat=True).distinct()
        if not bus_numbers:
            return Response({"status": 400, 'message': 'Bus not found'})

        result = [{'bus_number': bus_num} for bus_num in bus_numbers]
        
        return Response({'status': 200, 'data': result})