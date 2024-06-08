from datetime import datetime, time
from rest_framework.response import Response

from bus_routing.models import Deposit, Ticket
from bus_routing.serializer import DepositSerializer, TicketSerializer, TicketStationSerializer
from rest_framework import views


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
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        price = data.get('price')
        bus_number = data.get('bus_number')
        ticket_station_data = data.get('ticket_station_data')
        if not user_id or not price:
            return Response({"status" : 400, 'message': 'user_id, price, bus_number are required'})
        try:
            deposit = Deposit.objects.get(user_id=user_id)
            if deposit.amount >= price:
                deposit.amount -= price
                deposit.save()
            else:
                return Response(status=400, data = {"status" : 400, 'message': 'amount not enough'})
        except: 
            return Response(status=400, data = {"status" : 400, 'message': 'Deposit not found'})
        today = datetime.now().date()
        end_of_day = datetime.combine(today, time(23, 59, 0))

        ticket_data = {
            'user_id': user_id,
            'bus_number': bus_number,
            'price': price,
            'status': 0,
            'valid_to': end_of_day
        }
        ticket_serializer = TicketSerializer(data=ticket_data)
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            ticket_id = ticket_serializer.data.get('ticket_id')
            try:
                for ticket_station_info in ticket_station_data:
                    ts_info = {
                        'ticket_id': ticket_id,
                        'bus_number': ticket_station_info.get('bus_number'),
                        'on_bus_station_id': ticket_station_info.get('on_bus_station_id'),
                        'off_bus_station_id': ticket_station_info.get('off_bus_station_id')
                    }
                    ticket_station_serializer = TicketStationSerializer(data=ts_info)
                    if ticket_station_serializer.is_valid():
                        ticket_station_serializer.save()            
            except:
                return Response(status=400, data = {"status" : 400, 'message': 'TicketStation information is not correct'})

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
    
