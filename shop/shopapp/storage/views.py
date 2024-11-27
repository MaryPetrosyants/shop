from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from shopapp.storage.models import Storage, StorageProduct
from shopapp.storage.serializers import StorageSerializer, StorageProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shopapp.error_schema import error_schema_400, error_schema_403, error_schema_404, error_schema_500
class StorageView(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']


    @swagger_auto_schema(
        operation_summary="All storages",
        responses={
            200: StorageSerializer,
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Create a new Srorage object",
        responses={
            200: StorageSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        })
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    



    @swagger_auto_schema(
        operation_summary="Update Srorage object",
        responses={
            200: StorageSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Update Srorage object",
        responses={
            200: StorageSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Get Srorage object by Id",
        responses={
            200: StorageSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    



    @swagger_auto_schema(
        operation_summary="Delete Srorage object",
        responses={
            200: StorageSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    



class StorageProductView(viewsets.ModelViewSet):
    queryset = StorageProduct.objects.all()
    serializer_class = StorageProductSerializer




    @swagger_auto_schema(
        operation_summary="All product in the storages",
        responses={
            200: StorageProductSerializer,
            500: error_schema_500,
        }
    )
    @method_decorator(cache_page(60 * 15), 'dispatch')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary="Create a new Srorage Product object",
        responses={
            200: StorageProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    



    @swagger_auto_schema(
        operation_summary="Update Srorage Product object",
        responses={
            200: StorageProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    



    @swagger_auto_schema(
        operation_summary="Delete Srorage Product object",
        responses={
            200: StorageProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Get Srorage Product object by Id",
        responses={
            200: StorageProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Srorage Product object",
        responses={
            200: StorageProductSerializer,
            400: error_schema_400,
            403: error_schema_403,
            404: error_schema_404,
            500: error_schema_500,
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
