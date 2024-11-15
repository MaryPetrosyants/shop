from django.urls import path, include
from .views import ProductView
from rest_framework.routers import DefaultRouter, SimpleRouter


router = SimpleRouter()
router.register(r'product', ProductView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
