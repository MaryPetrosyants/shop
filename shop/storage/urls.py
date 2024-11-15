from django.urls import path, include
from storage.views import StorageView, StorageProductView
from rest_framework.routers import DefaultRouter, SimpleRouter
router = DefaultRouter()
router.register(r'storage', StorageView, basename='storage')
router.register(r'storage-product', StorageProductView, basename='storage-product')
urlpatterns = [
    path('', include(router.urls)),
]