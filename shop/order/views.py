from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderProductSerializer
from .models import Order, OrderProduct
from datetime import datetime
# Create your views here.

class OrderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user) 

class OrderProductView(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer