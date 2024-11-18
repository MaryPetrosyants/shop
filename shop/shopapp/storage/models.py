from django.db import models
from uuid import uuid4
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import User
from shopapp.product.models import Product

class Storage(models.Model):
    __tablename__ = 'storage'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField()
    address = models.CharField()

    class Meta:
        indexes = (HashIndex(fields=('id',)),)


class StorageProduct(models.Model):
    __tablename__ = 'storage_product'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True)
    stock = models.PositiveIntegerField()
