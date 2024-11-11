from django.db import models

# Create your models here.
from django.db import models
from uuid import uuid4
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import User
from product.models import Product


class Cart(models.Model):
    __tablename__ = 'cart'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        indexes = (HashIndex(fields=('id',)),)


class CartProduct(models.Model):
    __tablename__ = 'cart_product'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
