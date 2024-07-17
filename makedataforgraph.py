import googlemaps
import pymysql
import random
from datetime import datetime, timedelta

# Cấu hình Google Maps API
API_KEY = 'AIzaSyAnI_7dbzhe2FS7kr1lXvqXId2AIBvUXB8'
gmaps = googlemaps.Client(key=API_KEY)

# Cấu hình kết nối MySQL
db_config = {
    'user': 'root',
    'password': 'uxg',
    'host': 'localhost',
    'database': 'bus_routing'
}

# Hàm kết nối cơ sở dữ liệu
def connect_db():
    return pymysql.connect(**db_config)

# Đặt lại thời gian hiện tại về giờ tròn
def round_to_nearest_hour(dt):
    return dt.replace(minute=0, second=0, microsecond=0)

# Hàm xóa dữ liệu bảng
def clear_tables(cursor):
    cursor.execute("TRUNCATE TABLE bus_routing_buspassengerdata")
    cursor.execute("TRUNCATE TABLE bus_routing_checktickethistory")

# Hàm tạo dữ liệu cho bảng BusPassengerData
def create_bus_passenger_data(cursor):
    cursor.execute("SELECT DISTINCT bus_number, direction FROM bus_routing_busstation")
    bus_numbers = cursor.fetchall()
    current_time = round_to_nearest_hour(datetime.now())
    for bus_number, direction in bus_numbers:
        cursor.execute("SELECT bus_id, driver_name FROM bus_routing_bus WHERE bus_number=%s AND direction=%s", (bus_number, direction))
        bus_ids = cursor.fetchall()
        for bus_id, driver_name in bus_ids:
            for minute in range(0, 180, 5):
                passenger_amount = random.randint(0, 20)  # Số lượng hành khách ngẫu nhiên từ 0 đến 20
                timestamp = current_time - timedelta(minutes=minute)
                cursor.execute("""
                    INSERT INTO bus_routing_buspassengerdata (bus_number, direction, bus_id, driver_name, passenger_amount, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (bus_number, direction, bus_id, driver_name, passenger_amount, timestamp, timestamp))

# Hàm tạo dữ liệu cho bảng CheckTicketHistory
def create_check_ticket_history(cursor):
    cursor.execute("SELECT DISTINCT bus_number, direction FROM bus_routing_busstation")
    bus_numbers = cursor.fetchall()
    current_time = round_to_nearest_hour(datetime.now())
    for bus_number, direction in bus_numbers:
        cursor.execute("SELECT bus_id, driver_name FROM bus_routing_bus WHERE bus_number=%s AND direction=%s", (bus_number, direction))
        bus_ids = cursor.fetchall()
        for bus_id, driver_name in bus_ids:
            num_records = random.randint(100, 200)  # Số lượng bản ghi ngẫu nhiên từ 100 đến 200
            for _ in range(num_records):
                user_id = random.randint(1, 1000)  # user_id ngẫu nhiên
                ticket_id = random.randint(1, 500)  # ticket_id ngẫu nhiên
                days_ago = random.randint(0, 30)  # Ngày ngẫu nhiên trong 30 ngày qua
                minutes_ago = random.randint(0, 1440)  # Phút ngẫu nhiên trong ngày
                timestamp = current_time - timedelta(days=days_ago, minutes=minutes_ago)
                cursor.execute("""
                    INSERT INTO bus_routing_checktickethistory (user_id, direction, ticket_id, bus_id, driver_name, bus_number, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, direction, ticket_id, bus_id, driver_name, bus_number, timestamp, timestamp))

# Chạy các hàm tạo dữ liệu
def main():
    connection = connect_db()
    cursor = connection.cursor()
    
    clear_tables(cursor)
    create_bus_passenger_data(cursor)
    create_check_ticket_history(cursor)
    
    connection.commit()
    cursor.close()
    connection.close()

main()
