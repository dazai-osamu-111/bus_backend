import pymysql
import random
import string

# Cấu hình kết nối cơ sở dữ liệu
db_config = {
    'user': 'root',
    'password': 'uxg',
    'host': 'localhost',
    'database': 'busrouting'
}

# Hàm tạo biển số xe ngẫu nhiên
def generate_bus_number_plate():
    return '29' + random.choice(string.ascii_uppercase) + ''.join(random.choices(string.digits, k=5))

# Hàm nội suy vị trí giữa hai điểm
def interpolate_position(lat1, lon1, lat2, lon2):
    lat = random.uniform(lat1, lat2)
    lon = random.uniform(lon1, lon2)
    return lat, lon

# Kết nối tới cơ sở dữ liệu
connection = pymysql.connect(
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    database=db_config['database']
)

try:
    with connection.cursor() as cursor:
        print("Đã kết nối tới cơ sở dữ liệu")
        
        # Lấy dữ liệu từ bảng BusStation
        cursor.execute("select distinct bus_number, direction from bus_routing_busstation")
        bus_numbers = cursor.fetchall()

        cursor.execute("delete from bus_routing_bus")

        for bus_number, direction in bus_numbers:

            cursor.execute("SELECT latitude, longitude FROM bus_routing_busstation where bus_number=%s and direction=%s ORDER BY bus_station_id", (bus_number, direction))
            bus_stations = cursor.fetchall()

            # Tạo dữ liệu cho bảng Bus
            for _ in range(10):
                driver_name = generate_bus_number_plate()
                stop_index = random.randint(0, len(bus_stations) - 2)
                start_stop = bus_stations[stop_index]
                end_stop = bus_stations[stop_index + 1]
                
                latitude, longitude = interpolate_position(start_stop[0], start_stop[1], end_stop[0], end_stop[1])
                
                current_passenger_amount = random.randint(0, 20)  # Giả sử số lượng hành khách hiện tại ngẫu nhiên từ 0 đến 20
                max_passenger_amount = 20  # Giả sử số lượng hành khách tối đa là 20
                speed = random.uniform(10, 50)  # Giả sử tốc độ ngẫu nhiên từ 10 đến 50 km/h
                
                insert_bus_query = """
                INSERT INTO bus_routing_bus 
                (bus_number, driver_name, current_longitude, current_latitude, current_passenger_amount, max_passenger_amount, speed, direction, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """
                cursor.execute(insert_bus_query, (bus_number, driver_name, longitude, latitude, current_passenger_amount, max_passenger_amount, speed, direction))

            # Xác nhận các thay đổi
        connection.commit()

except Exception as e:
    print("Lỗi khi kết nối tới MySQL", e)
finally:
    connection.close()
    print("Đã đóng kết nối MySQL")
