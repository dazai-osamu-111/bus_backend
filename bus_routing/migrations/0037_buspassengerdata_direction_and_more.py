# Generated by Django 5.0.4 on 2024-07-17 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0036_rename_dirver_name_buspassengerdata_driver_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='buspassengerdata',
            name='direction',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checktickethistory',
            name='direction',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]