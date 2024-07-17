# Generated by Django 5.0.4 on 2024-07-17 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0032_remove_feedback_user_id_feedback_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusPassengerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_number', models.CharField(max_length=255)),
                ('bus_id', models.IntegerField()),
                ('passenger_amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='checkTicketHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('ticket_id', models.IntegerField()),
                ('bus_id', models.IntegerField()),
                ('bus_number', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
