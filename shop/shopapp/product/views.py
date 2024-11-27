from django.shortcuts import render
from rest_framework import viewsets
from shopapp.product.models import Product
from shopapp.product.serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from shopapp.error_schema import error_schema_400, error_schema_403, error_schema_404, error_schema_500

@method_decorator(cache_page(60*15), 'dispatch')
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(salesman=self.request.user)

    @swagger_auto_schema(
        operation_summary="All products",
        responses={
            200: ProductSerializer,
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new Product object",
        responses={
            200: ProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        })
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    
    @swagger_auto_schema(
        operation_summary="Update Product object",
        responses={
            200: ProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Product object",
        responses={
            200: ProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Product object",
        responses={
            200: ProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Product object by Id",
        responses={
            200: ProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
