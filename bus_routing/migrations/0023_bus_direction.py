# Generated by Django 5.0.4 on 2024-06-16 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0022_rename_bus_number_list_busstation_bus_number_list_go_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='direction',
            field=models.IntegerField(default=0),
        ),
    ]
