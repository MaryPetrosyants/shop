from django.contrib import admin

# Register your models here.
from .models import Storage, StorageProduct

admin.site.register(Storage)
admin.site.register(StorageProduct)