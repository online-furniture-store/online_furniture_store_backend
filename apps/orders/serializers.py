from django.db import transaction
from django.db.models import F, Sum
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

    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


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
        read_only_fields = ('user', 'total_cost')

    @staticmethod
    def update_storehouse(products):
        """Проверяет и обновляет кличество на складе после заказа."""

        storehouse = []
        for product in products:
            ordered_product = product.get('product')
            ordered_quantity = int(product.get('quantity'))
            storehouse_product = ordered_product.storehouse

            storehouse_product_quantity = storehouse_product.quantity
            if storehouse_product_quantity < ordered_quantity:
                raise ValidationError(
                    f'Для заказа товара {ordered_product} доступно {storehouse_product_quantity} шт.'
                )

            storehouse_product.quantity -= ordered_quantity
            storehouse.append(storehouse_product)

        Storehouse.objects.bulk_update(storehouse, ['quantity'])

    @staticmethod
    def add_products(order, products):
        """Сохраняет в базу данные заказа в OrderProduct, общую стоимость в Order."""

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

        order.total_cost = order.order_products.aggregate(Sum('cost'))['cost__sum']
        order.save()

    @transaction.atomic
    def create(self, validated_data):
        """Сохраняет заказ в базе, обрновляет склад."""

        products = validated_data.pop('products')
        self.update_storehouse(products)
        order = Order.objects.create(user=self.context.get('request').user, **validated_data)
        self.add_products(order, products)
        return order

    @transaction.atomic
    def update(self, order, validated_data):
        """Обновляет заказ и склад в базе."""

        products = validated_data.pop('products')
        self.increase_stock(order, products)
        order.products.clear()
        self.update_storehouse(products)
        self.add_products(order, products)
        return super().update(order, validated_data)

    @staticmethod
    def increase_stock(order, products):
        """Возвращает на склад количество товаров, удаляемых или обновляемых заказов."""

        Storehouse.objects.bulk_update(
            [
                Storehouse(
                    id=product['product'].id,
                    quantity=F('quantity') + order.order_products.get(product=product['product'].id).quantity,
                )
                for product in products
            ],
            ['quantity'],
        )

    def to_representation(self, instance):
        return OrderReadSerializer(instance, context={'request': self.context.get('request')}).data
