from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import Delivery, DeliveryType, Order, OrderProduct, Storehouse
from apps.product.models import Product


class DeliveryTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DeliveryType."""

    class Meta:
        model = DeliveryType
        fields = ('id', 'name')


class DeliverySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Delivery."""

    # TODO поле user
    # user = UserSerializer(read_only=True)
    type_delivery = DeliveryTypeSerializer

    class Meta:
        model = Delivery
        fields = ('id', 'address', 'phone', 'type_delivery', 'created', 'updated')

    def validate_phone(self, value):
        if not value:
            raise ValidationError('Укажите номер телефона для связи!')
        return value

    def validate_type_delivery(self, value):
        if not value:
            raise ValidationError('Укажите способ доставки!')
        return value

    def validate_address(self, value):
        if not value:
            raise ValidationError('Укажите адрес доставки')
        return value

    def validate(self, data):
        if 'type_delivery' not in data:
            raise ValidationError({'type_delivery': 'Обязательное поле'})
        return data


class OrderProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи товаров в заказе в модель OrderProduct."""

    id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    # cost = serializers.SerializerMethodField

    class Meta:
        model = OrderProduct
        fields = ('id', 'quantity')

    # def get_cost(self):
    #     return self.price * self.quantity


class OrderProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения товаров в заказе из модели OrderProduct."""

    id = serializers.ReadOnlyField(source='product.id')
    products = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderProduct
        fields = ('id', 'products', 'quantity', 'price', 'cost')


class OrderReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения Заказов из модели Order."""

    # TODO поле user
    # user = UserSerializer(read_only=True)
    products = serializers.SerializerMethodField()
    delivery = DeliverySerializer()

    class Meta:
        model = Order
        fields = ('id', 'user', 'products', 'delivery', 'total_cost', 'paid')

    def get_products(self, obj):
        queryset = OrderProduct.objects.filter(order=obj)
        return OrderProductReadSerializer(queryset, many=True).data


class OrderWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи Заказов в модель Order."""

    products = OrderProductWriteSerializer(many=True)
    delivery = serializers.PrimaryKeyRelatedField(queryset=Delivery.objects.all())

    class Meta:
        model = Order
        fields = ('id', 'products', 'delivery', 'paid')

    def validate_products(self, value):
        if not value:
            raise ValidationError('Минимальное количество товаров: 1!')
        product_list = []
        for item in value:
            product = get_object_or_404(Product, id=item['id'])
            quantity = int(item['quantity'])
            if product in product_list:
                raise ValidationError({'product': 'Товары не могут повторяться!'})
            if quantity <= 0:
                raise ValidationError({'quantity': 'Количество товаров должно быть больше 0!'})
            product_list.append(product)
        return value

    def validate_delivery(self, value):
        if Order.objects.filter(delivery=value).exists():
            raise ValidationError('Эта доставка уже используется')
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
        order = Order.objects.create(**validated_data)
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
        return OrderReadSerializer(instance, context=self.context).data
