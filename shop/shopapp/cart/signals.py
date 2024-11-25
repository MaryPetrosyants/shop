from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart, CartProduct


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=CartProduct)
@receiver(post_delete, sender=CartProduct)
def count_total_price(sender, instance, **kwargs):
    cart = instance.cart
    total_price = 0
    cart_products = CartProduct.objects.filter(cart=cart)
    for cart_product in cart_products:
        total_price += cart_product.product.price * cart_product.count

    cart.total_price = total_price
    cart.save()
