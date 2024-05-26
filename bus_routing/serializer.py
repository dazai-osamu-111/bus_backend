from rest_framework import serializers
from bus_routing.models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('user_id', 'amount')