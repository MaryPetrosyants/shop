from celery import shared_task
from datetime import datetime, timedelta
from .models import Order, OrderProduct
from shopapp.storage.models import StorageProduct


@shared_task
def delete_unconfirmed_orders():
    time_threshold = datetime.now() - timedelta(minutes=10)

    orders_to_delete = Order.objects.filter(
        status='NOT CONFIRMED',
        create_date__lt=time_threshold
    )
    for order in orders_to_delete:

        order_products = OrderProduct.objects.filter(order=order)
        for order_product in order_products:

            try:

                storage_product = StorageProduct.objects.filter(
                    product=order_product.product).first()
                storage_product.stock += order_product.count
                storage_product.save
            except StorageProduct.DoesNotExist:
                StorageProduct.objects.create(
                    product=order_product, stock=order_product.count)

        order_products.delete()
        order.delete()

    return f"Deleted unconfirmed orders"
