from rest_framework import serializers
from cart.models import Cart, CartProduct
from product.serializers import ProductSerializer


class CartProductSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'count']


class CartSerializer(serializers.ModelSerializer):
    cart_product = CartProductSerializer(
        many=True, source='cartproduct_set', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'cart_product']
        read_only_fields = ['id', 'user', 'total_price', 'cart_product']
