from rest_framework.response import Response

from bus_routing.models import Deposit
from bus_routing.serializer import DepositSerializer
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
        if not user_id or not price:
            return Response({"status" : 400, 'message': 'User_id and amount are required'})
        try:
            deposit = Deposit.objects.get(user_id=user_id)
            if deposit.amount >= price:
                deposit.amount -= price
                deposit.save()
                return Response({"status" : 200, 'message': 'Buy ticket successfully'})
            else:
                return Response({"status" : 400, 'message': 'amount not enough'})
        except: 
            return Response({"status" : 400, 'message': 'Deposit not found'})