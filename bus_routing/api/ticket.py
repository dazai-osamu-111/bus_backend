from bus_routing.models import Ticket
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CheckTicketView(APIView):
    def get(self, request):
        ticket_id = request.data.get('ticket_id')
        ticket = Ticket.objects.filter(ticket_id=ticket_id).first()
        if not ticket:
            return Response({'status': 400, 'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        ticket_status = ticket.status
        if ticket_status == 0:
            return Response({'status': 200, 'message': 'Ticket is valid'}, status=status.HTTP_200_OK)
        return Response({'status': 400, 'message': 'Ticket is invalid'}, status=status.HTTP_400_BAD_REQUEST)