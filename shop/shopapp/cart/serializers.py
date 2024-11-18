from rest_framework import serializers
from shopapp.cart.models import Cart, CartProduct
from shopapp.product.serializers import ProductSerializer
from django.contrib.auth.models import User


class CartProductSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'count']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CartSerializer(serializers.ModelSerializer):
    cart_product = CartProductSerializer(
        many=True, source='cartproduct_set', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'cart_product']
        read_only_fields = ['id', 'user', 'total_price', 'cart_product']
