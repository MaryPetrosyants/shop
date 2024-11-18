from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from shopapp.storage.models import Storage, StorageProduct
from shopapp.storage.serializers import StorageSerializer, StorageProductSerializer
from django_filters.rest_framework import DjangoFilterBackend


class StorageView(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class StorageProductView(viewsets.ModelViewSet):
    queryset = StorageProduct.objects.all()
    serializer_class = StorageProductSerializer