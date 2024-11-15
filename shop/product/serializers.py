from rest_framework import serializers
from product.models import Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'image', 'price', 'salesman']
        read_only_fields = ['id', 'category', 'name', 'description', 'image', 'price', 'salesman']
