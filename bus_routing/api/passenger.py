from django.db.models import Count
from rest_framework import views, response
from bus_routing.models import BusStation, BusPassengerData, checkTicketHistory
from datetime import datetime

class PassengerDataView(views.APIView):

    def get(self, request):
        # Lấy khoảng thời gian từ bản ghi đầu tiên và cuối cùng
        to_time = BusPassengerData.objects.all().order_by('created_at').first().created_at
        from_time = BusPassengerData.objects.all().order_by('created_at').last().created_at
        duration = from_time - to_time 

        # Tổng số hành khách
        sum_passenger = checkTicketHistory.objects.all().count()

        # Lấy các cặp bus_number và direction duy nhất
        distinct_bus_numbers = BusStation.objects.values('bus_number', 'direction').distinct()

        # Chuẩn bị dữ liệu cho biểu đồ
        graph_data = []
        for entry in distinct_bus_numbers:
            bus_number = entry['bus_number']
            direction = entry['direction']

            # Tạo giá trị route với "lượt đi" nếu direction bằng 0 và "lượt về" nếu direction bằng 1
            if direction == 0:
                route = f"{bus_number}(lượt đi)"
            elif direction == 1:
                route = f"{bus_number}(lượt về)"
            else:
                route = bus_number

            # Tính tổng số hành khách cho tuyến này
            total_passenger = checkTicketHistory.objects.filter(bus_number=bus_number, direction=direction).count()

            # Lấy dữ liệu hành khách cho từng thời điểm trong tuyến này
            time_data = BusPassengerData.objects.filter(bus_number=bus_number, direction=direction).values('created_at').annotate(total=Count('passenger_amount')).order_by('-created_at')

            route_graph_data = []
            for time_entry in time_data:
                time = time_entry['created_at']
                buses = BusPassengerData.objects.filter(bus_number=bus_number, direction=direction, created_at=time).values('driver_name', 'passenger_amount')[:5]  # Giới hạn 5 xe buýt

                bus_info = []
                for bus in buses:
                    driver_name = bus['driver_name']
                    passenger_count = bus['passenger_amount']
                    bus_info.append({
                        'bus_plate': driver_name,
                        'passenger_count': passenger_count
                    })

                route_graph_data.append({
                    'time': time.strftime("%Y:%m:%d %H:%M:%S"),
                    'buses': bus_info
                })

            graph_data.append({
                'route': route,
                'total_passenger': total_passenger,
                'graph_data': route_graph_data
            })

        # Trả về dữ liệu theo cấu trúc yêu cầu
        return response.Response({
            'from': from_time.strftime("%Y:%m:%d %H:%M:%S"),
            'to': to_time.strftime("%Y:%m:%d %H:%M:%S"),
            'duration': f"{round(duration.total_seconds() / 3600)}h",
            'sum_passenger': sum_passenger,
            'graph_data': graph_data
        })
