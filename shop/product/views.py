from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from product.models import Product 
from cart.models import Cart, CartProduct 
from product.serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal

class ProductView(viewsets.ModelViewSet):
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
    
    @action(detail=True, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request,pk=None):
        product = self.get_object()
        cart=Cart.objects.get(user=request.user)
        cart_product, create = CartProduct.objects.get_or_create(product=product, cart=cart)
        cart_product.count += 1
        cart_product.save()
        self.count_total_price(cart, product)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
    
    def count_total_price(self,  cart, product):
        cart_products = CartProduct.objects.filter(cart=cart)
        total_price = Decimal("0.00")
        for cart_product in cart_products:
            price=product.price 
            total_price += price 

        cart.total_price += total_price
        cart.save()



