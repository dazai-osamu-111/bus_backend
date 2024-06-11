# # sửa code sau:
# # from django.http import JsonResponse
# # from django.db.models import Count
# # from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
# # import datetime
# # from rest_framework import views
# # from bus_routing.models import Bus, MovementHistory

# # class PassengerDataView(views.APIView):

# #     def get(self, request, period, interval):
# #         now = datetime.datetime.now()
        
# #         if not interval.isdigit():
# #             return JsonResponse({'error': 'Invalid interval'}, status=400)
        
# #         if period not in ['hour', 'day', 'week', 'month']:
# #             return JsonResponse({'error': 'Invalid period'}, status=400)
        
# #         interval = int(interval)
        
# #         if period == 'hour':
# #             time_threshold = now - datetime.timedelta(hours=interval)
# #             result = MovementHistory.objects.filter(
# #                 created_at__gte=time_threshold
# #             ).annotate(
# #                 period=TruncHour('created_at')
# #             ).values('bus_id', 'period').annotate(
# #                 count=Count('user_id')
# #             ).order_by('bus_id', 'period')
            
# #         elif period == 'day':
# #             time_threshold = now - datetime.timedelta(days=interval)
# #             result = MovementHistory.objects.filter(
# #                 created_at__gte=time_threshold
# #             ).annotate(
# #                 period=TruncDay('created_at')
# #             ).values('bus_id', 'period').annotate(
# #                 count=Count('user_id')
# #             ).order_by('bus_id', 'period')
            
# #         elif period == 'week':
# #             time_threshold = now - datetime.timedelta(weeks=interval)
# #             result = MovementHistory.objects.filter(
# #                 created_at__gte=time_threshold
# #             ).annotate(
# #                 period=TruncWeek('created_at')
# #             ).values('bus_id', 'period').annotate(
# #                 count=Count('user_id')
# #             ).order_by('bus_id', 'period')
            
# #         elif period == 'month':
# #             time_threshold = now - datetime.timedelta(days=30*interval)
# #             result = MovementHistory.objects.filter(
# #                 created_at__gte=time_threshold
# #             ).annotate(
# #                 period=TruncMonth('created_at')
# #             ).values('bus_id', 'period').annotate(
# #                 count=Count('user_id')
# #             ).order_by('bus_id', 'period')
        
# #         else:
# #             return JsonResponse({'error': 'Invalid period'}, status=400)


# #         formatted_result = {}
# #         for entry in result:
# #             bus_id = entry['bus_id']
# #             period = str(entry['period'])
# #             count = entry['count']
            
# #             # Find the route for the bus_id
            
# #             route_id = Bus.objects.get(bus_id=bus_id).bus_number

# #             if route_id not in formatted_result:
# #                 formatted_result[route_id] = {}
# #             if bus_id not in formatted_result[route_id]:
# #                 formatted_result[route_id][bus_id] = {}

# #             formatted_result[route_id][bus_id][period] = count

# #         return JsonResponse(formatted_result)
# # hiện tại dữ liệu lượng hành khách theo giờ, ngày, tuần, tháng chưa dúng. Với giờ thì lấy unit=1h, ngày thì unit=1ngày, tuần, tháng tương tự. việc lọc dữ liệu cần thực hiện đếm tổng số hành khách trong 1 đơn vị unit kia. Ví dụ với dữ liệu hành khách lúc 9h thì tính tổng lượng hành khác từ 8h-9h, với dữ liệu hành khác của 






# viết code python kết hợp sử dụng google map api để xác nhận tọa độ của các địa điểm sau và insert vào trong bảng mysql:
# dữ liệu như sau:
# BX Gia Lâm
# 549 Nguyễn Văn Cừ
# Trường THPT Nguyễn Gia Thiều
# E3.1 Điểm trung chuyển Long Biên
# 50 Hàng Cót
# 28 Đường Thành
# Bệnh viện Phụ sản TW
# Bệnh viện Phụ sản Trung ương
# Tổng công ty Đường sắt Việt Nam
# Ga Hà Nội
# 78-80A Khâm Thiên
# 274-276 Khâm Thiên
# 142-144 Nguyễn Lương Bằng
# Gò Đống Đa
# 290 Tây Sơn
# Số 108 Nguyễn Trãi
# Chợ Thượng Đình
# ĐH Khoa học - Tự nhiên
# Cục Sở hữu trí tuệ
# Bách hóa Thanh Xuân
# Đại Học Hà Nội
# Công ty CP Công trình GT
# Học viện An Ninh nhân dân
# Học viện Bưu chính viễn thông
# Big C Hà Đông - Hồ Gươm Plaza
# Sở Tư pháp Hà Nội - Cầu Trắng Hà Đông
# Bưu điện Hà Đông
# 80 Quang Trung
# Nhà thi đấu Hà Đông
# 350 - 352 Quang Trung
# Giữa số 428 - 430 Quang Trung
# 530 - 532 Quang Trung
# 678 - 680 Quang Trung
# Nissan Hà Đông
# Đối diện Trường TH Kinh tế Hà Tây
# BX Yên Nghĩa



# BX Yên Nghĩa
# Trường trung cấp Kinh tế
# Đối diện Nissan Hà Đông
# 807 Quang Trung
# 707-709 Quang Trung, Hà Đông
# Ngã tư Quang Trung, Lê Trọng Tấn - Nhà ga La Khê
# Chợ La Khê
# Công ty CPLH Thực Phẩm
# Bệnh viện Đa khoa Hà Đông
# Bưu điện Hà Đông
# Sở Tư Pháp Hà Nội
# Ga Văn Quán
# Siêu thị Nguyễn Kim
# Đại học Kiến trúc Hà Nội
# Học viện An Ninh nhân dân
# Ga Phùng Khoang
# 517 Nguyễn Trãi
# Cục Cảnh Sát Môi Trường Bộ Công An
# Học viện Khoa học Xã hội
# Công ty Giày Thượng Đình
# Trường ĐH Khoa học tự nhiên
# Ga Thượng Đình
# 129T Nguyễn Trãi
# Trường Đại học Thuỷ Lợi
# Đại học Công Đoàn
# 83 Nguyễn Lương Bằng
# 221A-221B Khâm Thiên
# Đài tưởng niệm Khâm Thiên
# Cung VH Hữu Nghị Việt Xô
# 65 Quán Sứ
# Bệnh viện Việt Đức
# 115 Phùng Hưng
# Đối diện 16 Phùng Hưng
# Ô Quan Chưởng
# Tổng cục Hải Quan
# 358 Nguyễn Văn Cừ
# Đối diện 447 Ngọc Lâm
# BX Gia Lâm


# Bác Cổ
# Trạm trung chuyển xe buýt Trần Khánh Dư
# Đối diện Bệnh Viện Trung ương Quân đội 108 - Trần Hưng Đạo
# Đại học Khoa học tự nhiên
# Hè cạnh vườn hoa 19-8, đường Hai Bà Trưng
# Trung tâm thương mại Tràng Tiền Plaza
# Bệnh viện Hữu Nghị Việt Nam - Cu Ba6-8 Tràng Thi
# Bệnh viện Việt Đức
# Cửa Nam - Phố ẩm thực Tống Duy Tân
# Vườn hoa Lênin - Cột Cờ Hà Nội
# Bệnh viện Xanh Pôn
# Văn Miếu Quốc Tử Giám
# Nhà Thờ Hàng Bột
# Ngã 5 Ô Chợ Dừa
# 142-144 Nguyễn Lương Bằng
# Gò Đống Đa
# 290 Tây Sơn
# Số 108 Nguyễn Trãi
# Chợ Thượng Đình
# ĐH Khoa học - Tự nhiên
# Cục Sở hữu trí tuệ
# Bách hóa Thanh Xuân
# Đại Học Hà Nội
# Công ty CP Công trình GT
# Học viện An Ninh nhân dân
# Học viện Bưu chính viễn thông
# Big C Hà Đông - Hồ Gươm Plaza
# Sở Tư pháp Hà Nội - Cầu Trắng Hà Đông
# Bưu điện Hà Đông
# 80 Quang Trung
# Nhà thi đấu Hà Đông
# 350 - 352 Quang Trung
# Giữa số 428 - 430 Quang Trung
# 530 - 532 Quang Trung
# 678 - 680 Quang Trung
# Nissan Hà Đông
# Đối diện Trường TH Kinh tế Hà Tây
# BX Yên Nghĩa