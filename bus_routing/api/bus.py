
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