# Generated by Django 5.0.4 on 2024-07-10 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0030_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnBusPassengerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_id', models.IntegerField()),
                ('bus_number', models.CharField(max_length=255)),
                ('passenger_amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]