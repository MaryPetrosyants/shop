from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.serializers import CartSerializer, CartProductSerializer
from cart.models import Cart, CartProduct
from order.models import Order, OrderProduct
from storage.models import Storage, StorageProduct
from order.serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from decimal import Decimal

class CartView(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    

    @action(detail=True, methods=['post'], url_path='create-order')
    def create_order(self, request, pk=None):
        cart = self.get_object()
        cart_products = CartProduct.objects.filter(cart=cart)
        order = Order.objects.create(
            user=cart.user,
            total_price=cart.total_price,
        )

        order_products = []
        for cart_product in cart_products:
            order_products.append(OrderProduct(
                order=order,
                product=cart_product.product,
                count=cart_product.count
            ))
            storage_product = StorageProduct.objects.get(
                product=cart_product.product)
            storage_product.stock -= cart_product.count
            storage_product.save()
        print(storage_product.stock)
        OrderProduct.objects.bulk_create(order_products)
        order_serializer = OrderSerializer(order)
        CartProduct.objects.filter(cart=cart).delete()
        cart.total_price = Decimal("0.00")
        cart.save()
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='clear-cart')
    def clear_cart(self, request, pk=None):
        cart = self.get_object()
        CartProduct.objects.filter(cart=cart).delete()
        cart.total_price = Decimal("0.00")
        cart.save()
        return Response({"message": "Cart has been cleared."}, status=status.HTTP_204_NO_CONTENT)


class CartProductView(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    @action(detail=True, methods=['delete'], url_path='delete-from-cart')
    def delete_from_cart(self, request, pk=None):
        cart_product = self.get_object()
        if cart_product.count > 1:
            cart_product.count -= 1
            cart_product.save()
        else:
            cart_product.delete()
        return Response({"message": "Product removed from cart."}, status=status.HTTP_204_NO_CONTENT)
