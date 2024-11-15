from rest_framework import serializers
from product.models import Product
from django.contrib.auth.models import User

class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']




class ProductSerializer(serializers.ModelSerializer):
    salesman = SalesmanSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'image', 'price', 'salesman']
        read_only_fields = ['id', 'category', 'name', 'description', 'image', 'price', 'salesman']
