# Generated by Django 5.0.4 on 2024-07-17 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0034_checktickethistory_driver_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='buspassengerdata',
            name='dirver_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
