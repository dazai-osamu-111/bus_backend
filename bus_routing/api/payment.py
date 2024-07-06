from datetime import datetime, timedelta
import pytz
from rest_framework.response import Response

from bus_routing.models import Deposit, Ticket
from bus_routing.serializer import DepositSerializer, TicketSerializer
from rest_framework import views
from rest_framework.permissions import IsAuthenticated


class DepositView(views.APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        amount = data.get('amount')
        if not user_id or not amount:
            return Response({"status" : 400, 'message': 'User_id and amount are required'})
        try:
            deposit = Deposit.objects.get(user_id=user_id)
            if amount > 0:
                deposit.amount += amount
                deposit.save()
                return Response({"status" : 200, 'message': 'Deposit successfully'})
            else:
                return Response({"status" : 400, 'message': 'Deposit failed'})
        except: 
            data = {
                'user_id': user_id,
                'amount': amount
            }
            serializer = DepositSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status" : 200, 'message': 'Deposit successfully'})

    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            deposits = Deposit.objects.get(user_id=user_id)
            serializer = DepositSerializer(deposits)
            return Response(status=200, data = serializer.data)
        except:
            return Response({"status" : 400, 'message': 'Deposit not found'})
        
class BuyTicketView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user_id = request.user.id
        price = data.get('price')
        ticket_type = data.get('ticket_type')

        if not user_id or not price:
            return Response({"status" : 400, 'message': 'user_id, price, bus_number are required'})
        try:
            deposit = Deposit.objects.get(user_id=user_id)
            if deposit.amount >= price:
                deposit.amount -= price
                
            else:
                return Response(status=400, data = {"status" : 401, 'message': 'amount not enough'})
        except: 
            return Response(status=400, data = {"status" : 402, 'message': 'Deposit not found'})

        
        # Xử lý valid_to dựa trên ticket_type
        if ticket_type == 0:  # Vé tháng
            valid_to = datetime.now().replace(day=1) + timedelta(days=32)
            valid_to = valid_to.replace(day=1) - timedelta(days=1)  # Last day of current month
        elif ticket_type == 1:  # Vé ngày
            valid_to = datetime.now() + timedelta(days=365)
        else:
            return Response({"status" : 400, 'message': 'ticket_type must be in [0, 1]'})

        ticket_data = {
            'user_id': user_id,
            'price': price,
            'status': 0,
            'ticket_type': ticket_type,
            'valid_to': valid_to,
            'bus_number': ""
        }

        ticket_serializer = TicketSerializer(data=ticket_data)
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            deposit.save()
            return Response({"status" : 200, 'message': 'Buy ticket successfully'})
        else:
            print(ticket_serializer.errors)
            return Response(status=400, data = {"status" : 400, 'message': 'Buy ticket failed'})
        
       
    
    def put(self, request):
        data = request.data
        ticket_id = data.get('ticket_id')
        status = data.get('status', None)
        bus_id = data.get('bus_id', None)
        if status not in [0, 1, 2]:
            return Response({"status" : 400, 'message': 'status must be in [0, 1, 2]'})
        if not ticket_id or status is None:
            return Response({"status" : 400, 'message': 'ticket_id, status are required'})
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.status = status
            ticket.bus_id = bus_id
            ticket.save()
            if status == 2:
                deposit = Deposit.objects.get(user_id=ticket.user_id)
                deposit.amount += ticket.price
                deposit.save()
            return Response({"status" : 200, 'message': 'update ticket successfully'})
        except: 
            return Response({"status" : 400, 'message': 'ticket not found'})
    
