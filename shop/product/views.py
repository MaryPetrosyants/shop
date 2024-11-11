from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from product.models import Product 
from product.serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')  
        if category:
            queryset = queryset.filter(category=category) 
        return queryset

