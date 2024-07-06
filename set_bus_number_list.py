import pymysql
from datetime import datetime

db_config = {
    'user': 'root',
    'password': 'uxg',
    'host': 'localhost',
    'database': 'bus_routing'
}

def create_bus_number_list():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT distinct name FROM bus_routing_busstation;")
    data = cursor.fetchall()

    for row in data:
        cursor.execute("SELECT bus_number FROM bus_routing_busstation WHERE name = %s and direction=0", row[0])
        bus_numbers = cursor.fetchall()
        bus_number_list = []
        for bus_number in bus_numbers:
            bus_number_list.append(bus_number[0])
        bus_number_list_go = ','.join(bus_number_list)
        print(bus_number_list_go)
        cursor.execute("UPDATE bus_routing_busstation SET bus_number_list_go = %s WHERE name = %s;", (bus_number_list_go, row[0]))
        
        cursor.execute("SELECT bus_number FROM bus_routing_busstation WHERE name = %s and direction=1", row[0])
        bus_numbers = cursor.fetchall()
        bus_number_list = []
        for bus_number in bus_numbers:
            bus_number_list.append(bus_number[0])
        bus_number_list_return = ','.join(bus_number_list)
        print(bus_number_list_return)
        cursor.execute("UPDATE bus_routing_busstation SET bus_number_list_return = %s WHERE name = %s", (bus_number_list_return, row[0]))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_bus_number_list()