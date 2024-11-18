from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from shopapp.product.views import ProductView
from shopapp.order.views import OrderView, OrderProductView
from shopapp.cart.views import CartView, CartProductView
from shopapp.storage.views import StorageView, StorageProductView

from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version="v1",
        description="API for the Shop application",
        
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), 
)


router = DefaultRouter()
router.register(r'product', ProductView, basename='product')
router.register(r'order', OrderView, basename='order')
router.register(r'order-product', OrderProductView, basename='order-product')
router.register(r'cart', CartView, basename='cart')
router.register(r'cart-product', CartProductView, basename='cart-product')
router.register(r'storage', StorageView, basename='storage')
router.register(r'storage-product', StorageProductView, basename='storage-product')

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/v1/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    
    
    path('api/v1/', include(router.urls)),

   
    path('api/v1/accounts/', include('rest_registration.api.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
