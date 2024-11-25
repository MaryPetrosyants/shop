from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderReadSerializer, OrderProductSerializer, OrderUpdateSerializer
from .models import Order, OrderProduct
from shopapp.cart.models import Cart, CartProduct
from shopapp.storage.models import StorageProduct
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class OrderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'paid']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action in ['list']:
            return OrderReadSerializer
        elif self.action in ['update']:
            return OrderUpdateSerializer
        return OrderReadSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        order = Order.objects.create(
            user=user,
            total_price=cart.total_price,
        )
        cart_products = CartProduct.objects.filter(cart=cart)
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

        OrderProduct.objects.bulk_create(order_products)
        CartProduct.objects.filter(cart=cart).delete()
        order_serializer = OrderReadSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance.status = request.data.get("status")
        instance.save()

        self.perform_update(serializer)

        response_serializer = OrderReadSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='confirm-order')
    def confirm_order(self, request, pk=None):
        order = self.get_object()
        order.status = 'ACCEPTED'
        order.save()
        order_serializer = OrderReadSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class OrderProductView(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name']
