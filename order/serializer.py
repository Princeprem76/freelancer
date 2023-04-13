from rest_framework import serializers

from order.models import clientOrder, orderProgress
from user.serializer import UserNameSerial, InterestDataSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_category = InterestDataSerializer(read_only=True, many=True)

    class Meta:
        model = clientOrder
        fields = ['id', 'order_name', 'description', 'order_category', 'order_price', 'image', 'deadline',
                  'is_active_order']


class OrderDataSerializer(serializers.ModelSerializer):
    order_category = InterestDataSerializer(read_only=True, many=True)
    client = UserNameSerial(read_only=True, many=False)

    class Meta:
        model = clientOrder
        fields = ['id', 'client', 'order_name', 'description', 'order_category', 'order_price', 'image', 'deadline',
                  ]


class OrderApplicationSerial(serializers.ModelSerializer):
    freelancer = UserNameSerial(read_only=True, many=False)
    applicants = UserNameSerial(read_only=True, many=True)
    order = OrderSerializer(read_only=True, many=False)

    class Meta:
        model = orderProgress
        fields = ['id', 'order', 'freelancer', 'orderStatus', 'applicants']
