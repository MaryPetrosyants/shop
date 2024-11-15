from django.urls import path, include
from cart.views import CartView, CartProductView
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()
router.register(r'cart', CartView, basename='cart')
router.register(r'cart-product', CartProductView, basename='cart-product')
urlpatterns = [
    path('', include(router.urls)),
]