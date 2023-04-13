from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import clientOrder, orderProgress
from order.serializer import OrderSerializer, OrderApplicationSerial


class Orders(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data['order_name']
        description = data['description']
        category = data['oder_category']
        price = data['price']
        image = request.FILES.get('image', False)
        deadline = data['deadline']
        try:
            orders = clientOrder.objects.create(client_id=request.user.id, order_name=name, description=description,
                                                order_price=price, image=image, deadline=deadline)
            for i in category:
                orders.order_category.add(i)
                orders.save()
            return Response({'data': 'Order Created'}, status=status.HTTP_200_OK)

        except:
            return Response({'data': 'error!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        data = clientOrder.objects.filter(client_id=request.user.id)
        serializer = OrderSerializer(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )


class OrderApply(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        order_id = request.query_params.get('id')
        order_data, _ = orderProgress.objects.get_or_create(order_id=order_id)
        order_data.applicants.add(user_id)
        order_data.orderStatus = 1
        order_data.save()
        return Response({"data": 'Applied!'}, status=status.HTTP_200_OK, )


class ApplicationDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('id')
        order_data = orderProgress.objects.get(order_id=order_id)
        serializer = OrderApplicationSerial(order_data, many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )


class AssignApplication(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = request.query_params.get('id')
        order_data = orderProgress.objects.get(order_id=order_id)
        order_data.freelancer = request.data['user_id']
        order_data.orderStatus = 2
        order_data.save()
        return Response({"data": 'Applicant Assigned'}, status=status.HTTP_200_OK, )


class ChangeStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = request.query_params.get('id')
        order_data = orderProgress.objects.get(order_id=order_id)
        order_data.orderStatus = 3
        order = clientOrder.objects.get(id=order_id)
        order.is_active_order = False
        order.save()
        order_data.save()
        return Response({"data": 'Order Completed'}, status=status.HTTP_200_OK, )
