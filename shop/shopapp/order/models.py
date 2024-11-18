from django.db import models

# Create your models here.
from django.db import models
from uuid import uuid4
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import User
from shopapp.product.models import Product
import datetime

class Order(models.Model):
    STATUS = {
        "ACCEPTED": "ACCEPTED",
        "DELIVERY": "DELIVERY",
        "COMPLETED":"COMPLETED",
    }
    __tablename__ = 'order'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=STATUS, default='ACCEPTED')
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)
    create_date = models.DateField(default=datetime.date.today)

    class Meta:
        indexes = (HashIndex(fields=('id',)),)


class OrderProduct(models.Model):
    __tablename__ = 'order_product'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField()

