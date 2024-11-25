from rest_framework import serializers
from .models import OrderProduct, Order
from shopapp.product.serializers import ProductSerializer
from django.contrib.auth.models import User


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'count']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class OrderReadSerializer(serializers.ModelSerializer):
    order_product = OrderProductSerializer(
        many=True, read_only=True, source='orderproduct_set')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'create_date',
                  'paid', 'total_price', 'order_product']
        read_only_fields = fields


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status']
