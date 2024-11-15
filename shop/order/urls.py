from django.urls import path, include
from .views import OrderView, OrderProductView
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()
router.register(r'order', OrderView, basename='order')
router.register(r'order-product', OrderProductView, basename='order-product')
urlpatterns = [
    path('', include(router.urls)),
]