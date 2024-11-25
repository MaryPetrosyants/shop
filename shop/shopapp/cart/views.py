from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shopapp.cart.serializers import CartSerializer, CartCreateProductSerializer, CartReadProductSerializer
from shopapp.cart.models import Cart, CartProduct
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters


class CartView(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user

        return Cart.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        CartProduct.objects.filter(cart=cart).delete()
        cart.save()
        return Response({"message": "Cart has been cleared."}, status=status.HTTP_204_NO_CONTENT)


class CartProductView(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name']

    def get_serializer_class(self):
        if self.action in ['list']:
            return CartReadProductSerializer
        elif self.action in ['create', 'update']:
            return CartCreateProductSerializer
        return CartReadProductSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = serializer.validated_data['cart']
        product = serializer.validated_data['product']

        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'count': serializer.validated_data.get('count', 1)}
        )

        if not created:
            cart_product.count += serializer.validated_data.get('count', 1)
            cart_product.save()

        response_serializer = CartReadProductSerializer(cart_product)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):

        cart_product = self.get_object()
        if cart_product.count > 1:
            cart_product.count -= 1
            cart_product.save()
        else:
            cart_product.delete()
        response_serializer = CartReadProductSerializer(cart_product)
        return Response(response_serializer.data, status=status.HTTP_204_NO_CONTENT)
