from django.db import models

# create bus station model
class BusStation(models.Model):
    bus_station_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
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
    current_position = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusRouting(models.Model):
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_station = models.ForeignKey(BusStation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class OnBusData(models.Model):
    bus_id = models.IntegerField()
    user_id = models.IntegerField()
    start_bus_station_id = models.IntegerField()
    end_bus_station_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    bus_number = models.CharField(max_length=255)
    status = models.IntegerField() # 0: chua su dung, 1: da su dung, 2: đã hủy
    price = models.FloatField()
    valid_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


