from rest_framework import serializers

from order.models import clientOrder, orderProgress, orderFile
from user.serializer import UserNameSerial, InterestDataSerializer


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField("get_status")
    order_category = InterestDataSerializer(read_only=True, many=True)

    class Meta:
        model = clientOrder
        fields = ['id', 'order_name', 'description', 'order_category', 'order_price', 'image', 'deadline',
                  'is_active_order', 'status']

    def get_status(self, obj):
        o = orderProgress.objects.get(order_id=obj.id)
        return o.orderStatus


class OrderDataSerializer(serializers.ModelSerializer):
    order_category = InterestDataSerializer(read_only=True, many=True)
    client = UserNameSerial(read_only=True, many=False)
    status = serializers.SerializerMethodField("get_status")

    class Meta:
        model = clientOrder
        fields = ['id', 'client', 'order_name', 'description', 'order_category', 'order_price', 'image', 'deadline',
                  'status'
                  ]

    def get_status(self, obj):
        o = orderProgress.objects.get(order_id=obj.id)
        return o.orderStatus


class OrderApplicationSerial(serializers.ModelSerializer):
    freelancer = UserNameSerial(read_only=True, many=False)
    applicants = UserNameSerial(read_only=True, many=True)
    order = OrderSerializer(read_only=True, many=False)

    class Meta:
        model = orderProgress
        fields = ['id', 'order', 'freelancer', 'orderStatus', 'applicants']


class MyOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True, many=False)

    class Meta:
        model = orderProgress
        fields = ['id', 'order', 'orderStatus']


class OrderApplicantsCount(serializers.ModelSerializer):
    freelancer = UserNameSerial(read_only=True, many=False)

    class Meta:
        model = orderProgress
        fields = ['freelancer_count', 'orderStatus', 'freelancer']


class OrderFile(serializers.ModelSerializer):
    class Meta:
        model = orderFile
        fields = "__all__"
