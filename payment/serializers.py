from rest_framework import serializers

from order.models import clientOrder
from payment.models import Payment


class OrderNameSerial(serializers.ModelSerializer):
    class Meta:
        model = clientOrder
        fields = ['order_name']


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderNameSerial(read_only=True, many=True)

    class Meta:
        model = Payment
        fields = ['transactionId', 'amount', 'date', 'gateway', 'order']
