from django.db import models

# Create your models here.
from django.db import models
from uuid import uuid4
from django.contrib.postgres.indexes import HashIndex
from django.contrib.auth.models import User


class Product(models.Model):

    CATEGORY = {
        "LAPTOP": "LAPTOP",
        "SMARTPHONE": "SMARTPHONE",
    }

    __tablename__ = 'product'
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.CharField(choices=CATEGORY)
    name = models.CharField()
    description = models.CharField()
    image = models.ImageField(upload_to='products/images/', blank=False, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = (HashIndex(fields=('id',)),)
