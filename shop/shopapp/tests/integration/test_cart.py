# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth.models import User
# from shopapp.cart.models import Cart, CartProduct
# from shopapp.product.models import Product
# from django.urls import reverse


# class CartProductCreateTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='buyer', password='password')
#         self.product1 = Product.objects.create(name='Product 1', price=100)
#         self.product2 = Product.objects.create(name='Product 2', price=200)

#         self.client.force_authenticate(user=self.user)

#         self.cart = Cart.objects.create(user=self.user)

#         self.url = reverse('cart-list')

#     def test_create_cartproduct(self):




