from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class OrdersView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "successfully got orders"}, status=status.HTTP_200_OK)
