from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shopapp.cart.serializers import CartSerializer, CartCreateProductSerializer, CartReadProductSerializer
from shopapp.cart.models import Cart, CartProduct
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from shopapp.error_schema import error_schema_400, error_schema_403, error_schema_404, error_schema_500

class CartView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('user')

    @swagger_auto_schema(
        operation_summary="User cart info",
        responses={
            200: CartSerializer,
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Create a new Cart object",
        responses={
            200: CartSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    



    @swagger_auto_schema(
        operation_summary="Update Cart object",
        responses={
            200: CartSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Cart object",
        responses={
            200: CartSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Clear cart",
        responses={
            200: CartSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        CartProduct.objects.filter(cart=cart).delete()
        cart.save()
        order_serializer = CartSerializer(cart)
        return Response(order_serializer.data)

    @swagger_auto_schema(
        operation_summary="Get Cart object by Id",
        responses={
            200: CartSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class CartProductView(viewsets.ModelViewSet):
    queryset = CartProduct.objects.select_related('product', 'cart')
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name']

    def get_serializer_class(self):
        if self.action in ['list']:
            return CartReadProductSerializer
        elif self.action in ['create', 'update']:
            return CartCreateProductSerializer
        return CartReadProductSerializer
    
    @swagger_auto_schema(
        operation_summary="All cart products",
        responses={
            200: CartReadProductSerializer,
            
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new Cart Product object",
        responses={
            200: CartReadProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = serializer.validated_data['cart']
        product = serializer.validated_data['product']

        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'count': serializer.validated_data.get('count', 1)}
        )

        if not created:
            cart_product.count += serializer.validated_data.get('count', 1)
            cart_product.save()

        response_serializer = CartReadProductSerializer(cart_product)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)



    @swagger_auto_schema(
        operation_summary="Update Cart Product object",
        responses={
            200: CartReadProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Cart Product object",
        responses={
            200: CartReadProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Cart Product object",
        responses={
            200: CartReadProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def destroy(self, request, *args, **kwargs):

        cart_product = self.get_object()
        if cart_product.count > 1:
            cart_product.count -= 1
            cart_product.save()
        else:
            cart_product.delete()
        response_serializer = CartReadProductSerializer(cart_product)
        return Response(response_serializer.data, status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_summary="Get Cart Product object by Id",
        responses={
            200: CartReadProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
