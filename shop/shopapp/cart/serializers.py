from rest_framework import serializers
from shopapp.cart.models import Cart, CartProduct
from shopapp.product.serializers import ProductSerializer
from django.contrib.auth.models import User


class CartReadProductSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'count']


class CartCreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'count']
        read_only_fields = ['id']


class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CartSerializer(serializers.ModelSerializer):
    cart_product = CartReadProductSerializer(
        many=True, source='cartproduct_set', read_only=True)
    user = CartUserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'cart_product']
        read_only_fields = ['id', 'total_price']
