from rest_framework import serializers
from .models import OrderProduct, Order
from product.serializers import ProductSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = ['order', 'product','count']

class OrderSerializer(serializers.ModelSerializer):
    order_product = OrderProductSerializer(many=True, read_only=True, source='orderproduct_set')
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'create_date', 'paid', 'total_price', 'order_product']
        read_only_fields = ['id', 'user', 'create_date', 'paid', 'total_price']
