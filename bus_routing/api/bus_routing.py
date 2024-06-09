from rest_framework.response import Response


from rest_framework import views

from bus_routing.models import BusRouting
from bus_routing.serializer import BusRoutingSerializer

class BusRoutingView(views.APIView):
    def post(self, request):
        bus_number = request.data.get('bus_number')
        bus_station_id = request.data.get('bus_station_number')

        try:
            bus_route = BusRouting.objects.get(
                bus_id=bus_number,
                bus_station_id=bus_station_id
            )
            return Response({
                'message': 'Bus route is existed'
            }, status=400)
        except:
            data = {
                'bus_number': bus_number,
                'bus_station_id': bus_station_id
            }
            serializer = BusRoutingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Add bus route successfully'
                })
            else:
                return Response({
                    'message': 'Add bus route failed'
                }, status=400)