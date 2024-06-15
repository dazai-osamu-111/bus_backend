from django.db import models

# create bus station model
class BusStation(models.Model):
    bus_station_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bus_number = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    bus_number_list_go = models.CharField(max_length=255, null=True, blank=True)
    bus_number_list_return = models.CharField(max_length=255, null=True, blank=True)
    direction = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Deposit(models.Model):
    user_id = models.CharField(max_length=255)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.amount
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    bus_number = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255) # bien so xe
    current_passenger_amount = models.IntegerField(default=0)
    max_passenger_amount = models.IntegerField(default=20)
    speed = models.FloatField(default=20)
    current_longitude = models.FloatField(null=True, blank=True)
    current_latitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusRouting(models.Model):
    bus_number = models.CharField(max_length=255, null=True, blank=True)
    bus_station_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class OnBusData(models.Model):
    ticket_id = models.IntegerField()
    start_bus_station_id = models.IntegerField()
    end_bus_station_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    bus_number = models.CharField(max_length=255)
    bus_id = models.IntegerField(null=True)
    status = models.IntegerField() # 0: chua su dung, 1: dang su dung, 3: đã su dung, 4 da het han
    price = models.FloatField()
    valid_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TicketStation(models.Model):
    ticket_id = models.IntegerField()
    bus_number = models.CharField(max_length=255)
    on_bus_station_id = models.IntegerField()
    off_bus_station_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MovementHistory(models.Model):
    ticket_id = models.IntegerField(null=True)
    bus_id = models.IntegerField()
    user_id = models.IntegerField()
    on_bus_at = models.DateTimeField(null=True)
    off_bus_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
