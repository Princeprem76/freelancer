from rest_framework import serializers

from order.models import clientOrder, orderProgress
from user.serializer import UserNameSerial


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = clientOrder
        fields = '__all__'


class OrderApplicationSerial(serializers.ModelSerializer):
    freelancer = UserNameSerial(read_only=True, many=False)
    applicants = UserNameSerial(read_only=True, many=True)
    order = OrderSerializer(read_only=True, many=False)

    class Meta:
        model = orderProgress
        fields = ['id', 'order', 'freelancer', 'orderStatus', 'applicants']
