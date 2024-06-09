
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
        bus_number = data.get('bus_number')
        driver_name = data.get('driver_name')
        speed = data.get('speed', 20)
        current_position = data.get('current_position', None)

        if not bus_number or not driver_name or not speed:
            return Response({"status" : 400, 'message': 'bus_number, driver_name, speed are required'})
        try:
            bus = Bus.objects.get(bus_number=bus_number, driver_name=driver_name)
            bus_id = bus.bus_id
            on_bus_data = OnBusData.objects.filter(bus_id=bus_id)
            current_passenger_amount = 0
            if on_bus_data:
                current_passenger_amount = len(on_bus_data)
            data = {
                'bus_number': bus_number,
                'driver_name': driver_name,
                'speed': speed,
                'current_passenger_amount': current_passenger_amount,
                'current_position': current_position if current_position else '',
            }
            serializer = BusSerializer(bus,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status" : 200, 'message': 'Update bus successfully'})
            else:
                return Response({"status" : 400, 'message': 'Update bus failed'})
        except:
            return Response({"status" : 400, 'message': 'Bus not found'})
    def post(self, request):
        data = request.data
        bus_number = data.get('bus_number')
        driver_name = data.get('driver_name')
        if not bus_number or not driver_name:
            return Response({"status" : 400, 'message': 'bus_number'})
        current_bus_number_amount = len(list(Bus.objects.filter(bus_number=bus_number)))
        if current_bus_number_amount > 5:
            return Response({"status" : 400, 'message': 'bus_number amount is over quota'})
        try:
            bus = Bus.objects.get(bus_number=bus_number, driver_name=driver_name)
            return Response({"status" : 400, 'message': 'Bus is existed'})
        except: 
            data = {
                'bus_number': bus_number,
                'driver_name': driver_name,
            }
            serializer = BusSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status" : 200, 'message': 'Add bus successfully'})
            else:
                return Response({"status" : 400, 'message': 'Add bus failed'})
            
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