from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
import datetime
from rest_framework import views
from bus_routing.models import Bus, MovementHistory

class PassengerDataView(views.APIView):

    def get(self, request, period, interval):
        now = datetime.datetime.now()
        
        if not interval.isdigit():
            return JsonResponse({'error': 'Invalid interval'}, status=400)
        
        if period not in ['hour', 'day', 'week', 'month']:
            return JsonResponse({'error': 'Invalid period'}, status=400)
        
        interval = int(interval)
        
        if period == 'hour':
            time_threshold = now - datetime.timedelta(hours=interval)
            result = MovementHistory.objects.filter(
                created_at__gte=time_threshold
            ).annotate(
                period=TruncHour('created_at')
            ).values('bus_id', 'period').annotate(
                count=Count('user_id')
            ).order_by('bus_id', 'period')
            
        elif period == 'day':
            time_threshold = now - datetime.timedelta(days=interval)
            result = MovementHistory.objects.filter(
                created_at__gte=time_threshold
            ).annotate(
                period=TruncDay('created_at')
            ).values('bus_id', 'period').annotate(
                count=Count('user_id')
            ).order_by('bus_id', 'period')
            
        elif period == 'week':
            time_threshold = now - datetime.timedelta(weeks=interval)
            result = MovementHistory.objects.filter(
                created_at__gte=time_threshold
            ).annotate(
                period=TruncWeek('created_at')
            ).values('bus_id', 'period').annotate(
                count=Count('user_id')
            ).order_by('bus_id', 'period')
            
        elif period == 'month':
            time_threshold = now - datetime.timedelta(days=30*interval)
            result = MovementHistory.objects.filter(
                created_at__gte=time_threshold
            ).annotate(
                period=TruncMonth('created_at')
            ).values('bus_id', 'period').annotate(
                count=Count('user_id')
            ).order_by('bus_id', 'period')
        
        else:
            return JsonResponse({'error': 'Invalid period'}, status=400)


        formatted_result = {}
        for entry in result:
            bus_id = entry['bus_id']
            period = str(entry['period'])
            count = entry['count']
            
            # Find the route for the bus_id
            
            route_id = Bus.objects.get(bus_id=bus_id).bus_number

            if route_id not in formatted_result:
                formatted_result[route_id] = {}
            if bus_id not in formatted_result[route_id]:
                formatted_result[route_id][bus_id] = {}

            formatted_result[route_id][bus_id][period] = count

        return JsonResponse(formatted_result)
