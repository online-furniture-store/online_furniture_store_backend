from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import Delivery, DeliveryMethod, OrderProduct, Orders, Storehouse
from apps.product.models import Product


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
    # TODO поле user
    # user = UserSerializer(read_only)
    adres = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    type_delivery = serializers.PrimaryKeyRelatedField(queryset=DeliveryMethod.objects.all())

    class Meta:
        model = Delivery
        fields = ('id', 'adres', 'phone', 'type_delivery', 'created', 'updated')

    # def get_user(self, obj):
    #     user = self.context.get('request').user
    #     serializer = UserSerializer(user, read_only=True)
    #     return serializer.data


class StorehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storehouse
        fields = ('id', 'product', 'quantity')

    def validate_quantity(self, value):
        quantity = value
        if quantity < 0:
            raise ValidationError('Укажите значение больше или равное 0')
        return value


class OrderProductWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    cost = serializers.SerializerMethodField

    class Meta:
        model = OrderProduct
        fields = ('id', 'quantity', 'cost')

    def get_cost(self):
        return self.price * self.quantity


class OrderProductReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    products = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderProduct
        fields = ('id', 'products', 'quantity', 'price', 'cost')


class OrdersReadSerializer(serializers.ModelSerializer):
    # TODO поле user
    # user = UserSerializer(read_only)
    products = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    delivery = DeliverySerializer()

    class Meta:
        model = Orders
        fields = ('id', 'products', 'delivery', 'total_cost', 'paid')

    def get_products(self, obj):
        queryset = OrderProduct.objects.filter(order=obj)
        return OrderProductReadSerializer(queryset, many=True).data

    def get_total_cost(self, obj):
        return OrderProduct.objects.filter(order=obj).aggregate(Sum('cost'))['cost__sum']


class OrdersWriteSerializer(serializers.ModelSerializer):
    # TODO поле user
    products = OrderProductWriteSerializer(many=True)
    # user = UserSerializer(read_only)
    delivery = serializers.PrimaryKeyRelatedField(queryset=Delivery.objects.all())

    class Meta:
        model = Orders
        fields = ('id', 'products', 'delivery', 'paid')

    def validate_products(self, value):
        products = value
        if not products:
            raise ValidationError('Минимальное количество товаров: 1!')
        product_list = []
        for item in products:
            product = get_object_or_404(Product, id=item['id'])
            quantity = int(item['quantity'])
            if product in product_list:
                raise ValidationError({'product': 'Товары не могут повторяться!'})
            if quantity <= 0:
                raise ValidationError({'quantity': 'Количество товаров должно быть больше 0!'})
            product_list.append(product)
        return value

    @transaction.atomic
    def create_product_quantity(self, products, order):
        OrderProduct.objects.bulk_create(
            [
                OrderProduct(
                    product=Product.objects.get(id=product['id']),
                    price=Product.objects.get(id=product['id']).price,
                    quantity=product['quantity'],
                    order=order,
                    cost=Product.objects.get(id=product['id']).price * product['quantity'],
                )
                for product in products
            ]
        )

    @transaction.atomic
    def update_storehouse(self, products, order):
        for item in products:
            new_quantity = int(item['quantity'])
            current_quantity = get_object_or_404(OrderProduct, order=order).quantity
            product_storehouse = get_object_or_404(Storehouse, id=item['id'])
            quantity_storehouse = product_storehouse.quantity
            remains = quantity_storehouse + current_quantity - new_quantity
            product_storehouse.quantity = remains
            product_storehouse.save(update_fields=['quantity'])

    @transaction.atomic
    def create(self, validated_data):
        products = validated_data.pop('products')
        for item in products:
            product = get_object_or_404(Product, id=item['id'])
            new_quantity = int(item['quantity'])
            quantity_storehouse = get_object_or_404(Storehouse, id=item['id']).quantity
            if quantity_storehouse == 0:
                raise ValidationError(f'product: {product} -->> Товар закончился')
            if new_quantity >= quantity_storehouse:
                raise ValidationError(f'product: {product}: quantity: Не больше {quantity_storehouse}')
            product_storehouse = get_object_or_404(Storehouse, id=item['id'])
            product_storehouse.quantity = product_storehouse.quantity - new_quantity
            product_storehouse.save(update_fields=['quantity'])
        order = Orders.objects.create(**validated_data)
        self.create_product_quantity(order=order, products=products)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        for item in products:
            product = get_object_or_404(Product, id=item['id'])
            new_quantity = int(item['quantity'])
            current_quantity = get_object_or_404(OrderProduct, order=instance).quantity
            quantity_storehouse = get_object_or_404(Storehouse, id=item['id']).quantity
            remains = quantity_storehouse + current_quantity - new_quantity
            if remains < 0:
                raise ValidationError(f'product: {product} -->> quantity: На складе недостаточно товаров')
        self.update_storehouse(order=instance, products=products)
        instance = super().update(instance, validated_data)
        instance.products.clear()
        self.create_product_quantity(order=instance, products=products)
        instance.save()
        return instance

    def to_representation(self, instance):
        return OrdersReadSerializer(instance, context=self.context).data