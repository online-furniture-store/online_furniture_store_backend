from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.cart.cart import Cart
from apps.cart.serializers import CartSerializer
from apps.product.models import Product


class CartViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def view_cart(self, request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        # Получение данных из запроса, например, product_id и quantity
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Получение продукта из базы данных
        product = get_object_or_404(Product, id=product_id)
        # product = Product.objects.get(id=product_id)

        # Добавление товара в корзину
        cart = Cart(request)
        cart.add(product, quantity)

        # Возвращение данных корзины в ответе
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        # Получение данных из запроса, например, product_id
        product_id = request.data.get('product_id')

        # Получение продукта из базы данных
        product = Product.objects.get(id=product_id)

        # Удаление товара из корзины
        cart = Cart(request)
        cart.remove(product)

        # Возвращение данных корзины в ответе
        serializer = CartSerializer(cart)
        return Response(serializer.data)
