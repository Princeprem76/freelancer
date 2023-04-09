from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import Payment
from payment.serializers import PaymentSerializer


class Order_payment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        order = data['order_id']
        trans = data['transaction_id']
        amount = data['amount']
        gateway = data['gateway']
        Payment(client_id=request.user.id, order_id=order, transactionId=trans, amount=amount, gateway=gateway).save()
        return Response({'message': 'Payment Done'}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        data = Payment.objects.filter(client_id=request.user.id)
        serializer = PaymentSerializer(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )
