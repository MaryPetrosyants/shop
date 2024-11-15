from rest_framework import serializers
from storage.models import Storage, StorageProduct
class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class StorageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageProduct
        fields = '__all__'