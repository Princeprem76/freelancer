from rest_framework import serializers

from order.models import clientOrder


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = clientOrder
        fields = '__all__'
