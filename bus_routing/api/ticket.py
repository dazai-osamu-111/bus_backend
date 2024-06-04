import datetime
from urllib import response
from bus_routing.models import Ticket
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bus_routing.serializer import TicketSerializer


class CheckTicketView(APIView):

    def get(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({'status': 400, 'message': 'ticket_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        bus_number = request.data.get('bus_number')
        if not bus_number:
            return Response({'status': 400, 'message': 'bus_number is required'}, status=status.HTTP_400_BAD_REQUEST)
        ticket = Ticket.objects.filter(ticket_id=ticket_id).first()
        if not ticket:
            return Response({'status': 400, 'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        ticket_status = ticket.status
        ticket_bus_number = ticket.bus_number

        if ticket_status == 0 and bus_number in ticket_bus_number:
            return Response({'status': 200, 'message': 'Ticket is valid'}, status=status.HTTP_200_OK)
        return Response({'status': 400, 'message': 'Ticket is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    
class GetUserTicket(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        tickets = Ticket.objects.filter(user_id=user_id)
        serializer = TicketSerializer(tickets, many=True)
        response_data = {
            'status': 200,
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)