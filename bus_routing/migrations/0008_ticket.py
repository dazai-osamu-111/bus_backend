# Generated by Django 3.2.4 on 2024-06-02 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_routing', '0007_auto_20240528_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('bus_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('price', models.FloatField()),
                ('valid_to', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
