from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import Order
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.
class OrdersView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "successfully got orders"}, status=status.HTTP_200_OK)


class  CreateListOderView(generics.GenericAPIView):
    serializer_class = serializers.OderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        user = request.user

        if serializer.is_valid():
            serializer.save(customer=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, order_id):
        data = request.data

        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, render, order_id):
        # Fetch the order object, returning a 404 response if not found
        order = get_object_or_404(Order, pk=order_id)

        # Perform the deletion
        order.delete()

        # Return a 204 No Content response (Recommended for DELETE operations)
        # return Response(status=status.HTTP_204_NO_CONTENT)

        # Return a 200 (my prefered respose)
        return Response(data={'message': 'Order successfully deleted'}, status=status.HTTP_200_OK)


class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = serializers.OderStatusUpdateSerializer

    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        
        data = request.data

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data={'message': 'Order successfully updated order status'}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetUserOderView(generics.GenericAPIView):
    serializer_class = serializers.OderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        order = Order.objects.all().filter(customer = user)

        serializer = self.serializer_class(instance=order, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserOderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OderDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)

        order = Order.objects.all().filter(customer = user).get(pk=order_id)

        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
