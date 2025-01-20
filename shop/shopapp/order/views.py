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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from shopapp.error_schema import error_schema_400, error_schema_403, error_schema_404, error_schema_500
from django.core.cache import cache

cache.clear()

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
    
    @swagger_auto_schema(
        operation_summary="All user orders",
        responses={
            200: OrderReadSerializer,
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Create a new Order object",
        responses={
            200: OrderReadSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def create(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        order = Order.objects.create(
            user=user,
            total_price=cart.total_price,
        )
        cart_products = CartProduct.objects.filter(cart=cart).select_related('product')
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


    @swagger_auto_schema(
        operation_summary="Update Order object",
        responses={
            200: OrderReadSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can update orders.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance.status = request.data.get("status")
        instance.save()

        self.perform_update(serializer)

        response_serializer = OrderReadSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

    @swagger_auto_schema(
        operation_summary="Update Order object",
        responses={
            200: OrderReadSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Order object",
        responses={
            200: OrderReadSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )   
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Order object by Id",
        responses={
            200: OrderReadSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Confirm order",
        responses={
            200: OrderReadSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    @action(detail=True, methods=['post'], url_path='confirm-order')
    def confirm_order(self, request, pk=None):
        order = self.get_object()
        order.status = 'ACCEPTED'
        order.save()
        order_serializer = OrderReadSerializer(order)
        return Response(order_serializer.data)


class OrderProductView(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.select_related('product', 'order')
    serializer_class = OrderProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name']


    @swagger_auto_schema(
        operation_summary="All order products",
        responses={
            200: OrderProductSerializer,
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Create a new Order Product object",
        responses={
            200: OrderProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    



    @swagger_auto_schema(
        operation_summary="Update Order Product object",
        responses={
            200: OrderProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Order Product object",
        responses={
            200: OrderProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Order Product object",
        responses={
            200: OrderProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Order Product object by Id",
        responses={
            200: OrderProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

