from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.product.models import Product

from .models import Delivery, DeliveryMethod, Orders, ProductsOrder, Storehouse


class DeliveryMethodSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20)

    class Meta:
        model = DeliveryMethod
        fields = ('id', 'name')

    def validate_name(self, value):
        method = value
        if DeliveryMethod.objects.filter(name=method).exists():
            raise ValidationError('Такой способ доставки уже есть!')
        return value


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id', 'adres', 'phone', 'type_delivery', 'created')


class ProductOrderReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = ProductsOrder
        fields = ('id', 'product', 'amount')


class ProductOrderWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductsOrder
        fields = ('id', 'amount')


class OrdersReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'date', 'user', 'products', 'delivery', 'created', 'total')

    def get_products(self, obj):
        queryset = ProductsOrder.objects.filter(order=obj)
        return ProductOrderReadSerializer(queryset, many=True).data


class OrdersWriteSerializer(serializers.ModelSerializer):
    product = ProductOrderWriteSerializer(many=True)
    delivery = serializers.PrimaryKeyRelatedField(queryset=DeliveryMethod.objects.all())

    class Meta:
        model = Orders
        fields = ('date', 'user', 'products', 'delivery', 'created')

    def validate_product(self, value):
        products = value
        if not products:
            raise ValidationError({'products': 'Нужен хотя бы один товар!'})
        products_list = []
        for item in products:
            product = get_object_or_404(Product, id=item['id'])
            if product in products_list:
                raise ValidationError({'product': 'Товары не могут повторяться!'})
            products_list.append(product)
        return value

    def validate_delivery(self, value):
        delivery = value
        if not delivery:
            raise ValidationError({'delivery': 'Выберете способ доставки'})
        if len(delivery) > 1:
            raise ValidationError({'delivery': 'Выберете только 1 способ доставки!'})


class StorehouseSerializer(serializers.ModelSerializer):
    # product = serializers.IntegerField(read_only=True)

    class Meta:
        model = Storehouse
        fields = ('id', 'products', 'amount')

    # def validate_product(self, value):
    #     product = value
    #     if not product:
    #         raise ValidationError({
    #             'product': 'Выберете товар'
    #         })
    #     return value


class StorehouseReadSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.id')

    class Meta:
        model = Storehouse
        fields = ('id', 'product', 'amount')
