from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import Delivery, DeliveryType, Order, OrderProduct, Storehouse


class DeliveryTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DeliveryType."""

    class Meta:
        model = DeliveryType
        fields = ('id', 'name')


class DeliverySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Delivery."""

    type_delivery = serializers.PrimaryKeyRelatedField(queryset=DeliveryType.objects.all(), allow_null=True)

    class Meta:
        model = Delivery
        fields = ('id', 'address', 'phone', 'type_delivery', 'created', 'updated')


class OrderProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи товаров в заказе в модель OrderProduct."""

    quantity = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')

    def validate_quantity(self, value):
        if value <= 0:
            value = 1
        return value


class OrderProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения товаров в заказе из модели OrderProduct."""

    id = serializers.ReadOnlyField(source='product.id')
    products = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderProduct
        fields = ('id', 'products', 'quantity', 'price', 'cost')


class OrderReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения Заказов из модели Order."""

    products = OrderProductReadSerializer(many=True, source='order_products')
    delivery = DeliverySerializer()

    class Meta:
        model = Order
        fields = ('id', 'user', 'products', 'delivery', 'total_cost', 'paid')


class OrderWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи Заказов в модель Order."""

    products = OrderProductWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'products', 'delivery', 'total_cost', 'paid')
        read_only_fields = ('user',)

    @transaction.atomic
    def add_products(self, order, products):
        OrderProduct.objects.bulk_create(
            [
                OrderProduct(
                    order=order,
                    product=product.get('product'),
                    price=product.get('product').price,
                    quantity=product['quantity'],
                    cost=product.get('product').price * product['quantity'],
                )
                for product in products
            ]
        )

    @transaction.atomic
    def update_storehouse(self, order, products):
        for product in products:
            new_quantity = int(product['quantity'])
            current_quantity = get_object_or_404(OrderProduct, order=order, product=product.get('product')).quantity
            product_storehouse = get_object_or_404(Storehouse, product=product.get('product'))
            quantity_storehouse = product_storehouse.quantity
            remains = quantity_storehouse + current_quantity - new_quantity
            product_storehouse.quantity = remains
            product_storehouse.save(update_fields=['quantity'])

    @transaction.atomic
    def create(self, validated_data):
        products = validated_data.pop('products')
        for new_product in products:
            product = new_product.get('product')
            new_quantity = int(new_product['quantity'])
            product_storehouse = get_object_or_404(Storehouse, product=product)
            quantity_storehouse = product_storehouse.quantity
            if quantity_storehouse == 0:
                raise ValidationError(f'product: {product} -->> Товар закончился')
            if new_quantity > quantity_storehouse:
                raise ValidationError(f'product: {product}: quantity: Не больше {quantity_storehouse}')

            product_storehouse.quantity = product_storehouse.quantity - new_quantity
            product_storehouse.save(update_fields=['quantity'])
        order = Order.objects.create(user=self.context.get('request').user, **validated_data)
        self.add_products(order=order, products=products)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        for new_product in products:
            product = new_product.get('product')
            new_quantity = int(new_product['quantity'])
            if not OrderProduct.objects.filter(order=instance, product=product).exists():
                price = product.price
                OrderProduct.objects.create(order=instance, product=product, price=price, quantity=new_quantity)
            current_quantity = get_object_or_404(OrderProduct, order=instance, product=product).quantity
            quantity_storehouse = get_object_or_404(Storehouse, product=product).quantity
            remains = quantity_storehouse + current_quantity - new_quantity
            if remains < 0:
                raise ValidationError(f'product: {product} -->> quantity: На складе недостаточно товаров')
        self.update_storehouse(order=instance, products=products)
        instance = super().update(instance, validated_data)
        instance.products.clear()
        self.add_products(order=instance, products=products)
        instance.total_cost = OrderProduct.objects.filter(order=instance).aggregate(Sum('cost'))['cost__sum']
        instance.save()
        return instance

    def to_representation(self, instance):
        return OrderReadSerializer(instance, context={'request': self.context.get('request')}).data
