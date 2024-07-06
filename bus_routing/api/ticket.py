import datetime

import pytz
from bus_routing.models import Bus, BusStation, Ticket
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from bus_routing.serializer import TicketSerializer


class CheckTicketView(APIView):

    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({'status': 400, 'message': 'ticket_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        bus_id = request.data.get('bus_id')
        bus_number = request.data.get('bus_number')
        if not bus_number:
            return Response({'status': 400, 'message': 'bus_number is required'}, status=status.HTTP_400_BAD_REQUEST)
        ticket = Ticket.objects.filter(ticket_id=ticket_id).first()
        if not ticket:
            return Response({'status': 400, 'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        ticket_status = ticket.status
        ticket_type = ticket.ticket_type
        valid_to = ticket.valid_to
        bus_station_object = BusStation.objects.filter(bus_number=bus_number).first()
        bus_object = Bus.objects.filter(bus_id=bus_id).first()
        if not bus_object:
            return Response({'status': 400, 'message': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        if bus_station_object:
            bus_price = bus_station_object.price
        else:
            bus_price = 0
        now = datetime.datetime.now(pytz.utc)

        if ticket_type == 0:
            if valid_to > now:
                current_passenger_amount = bus_object.current_passenger_amount
                current_passenger_amount += 1
                bus_object.current_passenger_amount = current_passenger_amount
                bus_object.save()
                
                return Response({'status': 200, 'message': 'Ticket is valid'}, status=status.HTTP_200_OK)
        else:
            if valid_to > now:
                if ticket_status == 0:
                    if bus_price == ticket.price:
                        current_passenger_amount = bus_object.current_passenger_amount
                        current_passenger_amount += 1
                        bus_object.current_passenger_amount = current_passenger_amount
                        bus_object.save()
                        ticket.status = 1
                        ticket.save()

                        return Response({'status': 200, 'message': 'Ticket is valid'}, status=status.HTTP_200_OK)
                else:    
                    return Response({'status': 400, 'message': 'Ticket was used'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 400, 'message': 'Ticket is expired'}, status=status.HTTP_400_BAD_REQUEST)
    
class GetUserTicket(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        ticket_type = request.query_params.get('ticket_type')
        status = request.query_params.get('status')
        tickets = Ticket.objects.filter(user_id=user_id, ticket_type=ticket_type, status = status)
        if not tickets:
            return Response({'status': 400, 'message': 'Ticket not found'}, status=400)
        serializer = TicketSerializer(tickets, many=True)
        response_data = {
            'status': 200,
            'data': serializer.data
        }
        return Response(response_data, status=200)