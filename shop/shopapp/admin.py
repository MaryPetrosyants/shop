from django.contrib import admin
from shopapp.product.models import Product
from shopapp.order.models import Order, OrderProduct
from shopapp.cart.models import Cart, CartProduct
from shopapp.storage.models import Storage, StorageProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Storage)
admin.site.register(StorageProduct)
