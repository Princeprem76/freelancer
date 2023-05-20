import json

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import clientOrder, orderProgress, orderFile
from order.serializer import OrderSerializer, OrderApplicationSerial, OrderDataSerializer, OrderApplicantsCount, \
    MyOrderSerializer, OrderFile


class Orders(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data['order_name']
        description = data['description']
        category = request.POST.get('order_category', False)
        price = data['price']
        image = request.FILES.get('image', False)
        deadline = data['deadline']
        try:
            orders = clientOrder.objects.create(client_id=request.user.id, order_name=name, description=description,
                                                order_price=price, image=image, deadline=deadline)
            order_data = orderProgress.objects.create(order_id=orders.id)
            order_data.orderStatus = 1
            order_data.save()
            order_file = orderFile.objects.create(order_id=orders.id)
            d = json.loads(category)
            for i in d:
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
        order_id = kwargs['id']
        order_data, _ = orderProgress.objects.get_or_create(order_id=order_id)
        order_data.applicants.add(user_id)
        order_data.orderStatus = 1
        order_data.save()
        return Response({"data": 'Applied!'}, status=status.HTTP_200_OK, )


class ApplicationDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        order_id = kwargs['id']
        order_data = orderProgress.objects.get(order_id=order_id)
        serializer = OrderApplicationSerial(order_data, many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )


class AssignApplication(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = kwargs['id']
        order_data = orderProgress.objects.get(order_id=order_id)
        order_data.freelancer = request.data['user_id']
        order_data.orderStatus = 2
        order_data.save()
        return Response({"data": 'Applicant Assigned'}, status=status.HTTP_200_OK, )


class ChangeStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = kwargs['id']
        order_data = orderProgress.objects.get(order_id=order_id)
        order_data.orderStatus = 3
        order = clientOrder.objects.get(id=order_id)
        order.is_active_order = False
        order.save()
        order_data.save()
        return Response({"data": 'Order Completed'}, status=status.HTTP_200_OK, )


class SearchOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        interests = request.data['interest']
        data = clientOrder.objects.filter(order_category__interests__icontains=interests, is_active_order=True)
        serializer = OrderDataSerializer(data, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class AllOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = clientOrder.objects.filter(is_active_order=True)
        serializer = OrderDataSerializer(data, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class MyOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = orderProgress.objects.filter(freelancer_id=request.user.id)
        serializer = MyOrderSerializer(data, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class UploadFile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        files = request.FILES.get('file', False)
        order_id= request.data['order_id']
        data = orderFile.objects.get_or_create(order_id=order_id)
        data.files = files
        data.save()
        return Response({"data": 'File Added'}, status=status.HTTP_200_OK,)

    def get(self, request, *args, **kwargs):
        order_id = kwargs['id']
        data = orderFile.objects.get(order_id=order_id)
        serializer = OrderFile(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK, )

