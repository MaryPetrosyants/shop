from django.db import models
from uuid import uuid4
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import User
from shopapp.product.models import Product
from django.utils.timezone import now


class Order(models.Model):
    STATUS = {
        "NOT CONFIRMED":  "NOT CONFIRMED",
        "ACCEPTED": "ACCEPTED",
        "DELIVERY": "DELIVERY",
        "COMPLETED": "COMPLETED",
    }
    __tablename__ = 'order'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=STATUS, default='NOT CONFIRMED')
    total_price = models.DecimalField(
        max_digits=6, decimal_places=2, default='0.00')
    paid = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=now)

    class Meta:
        indexes = (HashIndex(fields=('id',)),)

    def __str__(self) -> str:
        return f"Order {self.user.username} - {self.create_date}"


class OrderProduct(models.Model):
    __tablename__ = 'order_product'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.product.name}"
