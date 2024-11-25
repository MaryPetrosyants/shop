from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from shopapp.storage.models import Storage, StorageProduct
from shopapp.storage.serializers import StorageSerializer, StorageProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# @method_decorator(cache_page(60*15), 'dispatch')
class StorageView(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

class StorageProductView(viewsets.ModelViewSet):
    queryset = StorageProduct.objects.all()
    serializer_class = StorageProductSerializer