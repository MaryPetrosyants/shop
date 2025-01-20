from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shopapp.order.models import Order, OrderProduct
from shopapp.cart.models import Cart, CartProduct
from shopapp.storage.models import StorageProduct, Storage
from shopapp.product.models import Product
from django.contrib.auth.models import User


class OrderTestCase(APITestCase):
    fixtures = ['shopapp/fixtures/test_data.json']

    def setUp(self):
        self.client.force_authenticate(user=self._get_user())
        self.url = reverse('order-list')

    def _get_user(self):
        return User.objects.get(username='testuser')

    def test_create_order(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.filter(user=self._get_user()).last()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 200)

        order_products = OrderProduct.objects.filter(order=order)
        self.assertEqual(order_products.count(), 1)
        self.assertEqual(order_products.first().count, 2)

        self.assertFalse(CartProduct.objects.filter(
            cart=Cart.objects.get(pk=1)).exists())

        storage_product = StorageProduct.objects.get(pk=1)
        self.assertEqual(storage_product.stock, 8)

    def test_read_order(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        orders = response.json()
        count = orders['count']
        self.assertEqual(count, 2)

    def test_update_order(self):
        admin_user = User.objects.get(username='adminuser')
        self.client.force_authenticate(user=admin_user)

        order = Order.objects.get(pk=1)
        print(order.pk)
        url = reverse('order-detail', args=[order.pk])
        print(url)
        data = {
            "status": "DELIVERY"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "DELIVERY")
    # def test_delete_order(self):

    # def test_confirm_order(self):
