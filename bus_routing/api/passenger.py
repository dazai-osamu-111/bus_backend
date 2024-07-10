from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
import datetime
from rest_framework import views
from bus_routing.models import Bus

class PassengerDataView(views.APIView):

    def get(self, request, period, interval):
        return