# Generated by Django 5.0.4 on 2024-06-16 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0024_rename_bus_station_id_busrouting_direction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='busstation',
            name='bus_number_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
