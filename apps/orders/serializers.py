from django.db import transaction
from django.db.models import Sum
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

    type_delivery = DeliveryTypeSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ('id', 'address', 'phone', 'type_delivery', 'created', 'updated')
        extra_kwargs = {
            'address': {'required': True},
            'phone': {'required': True},
            'type_delivery': {'required': True},
        }


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
        for product in products:
            new_quantity = int(product['quantity'])
            current_quantity = get_object_or_404(OrderProduct, order=order, product=product['id']).quantity
            product_storehouse = get_object_or_404(Storehouse, id=product['id'])
            quantity_storehouse = product_storehouse.quantity
            remains = quantity_storehouse + current_quantity - new_quantity
            product_storehouse.quantity = remains
            product_storehouse.save(update_fields=['quantity'])

    @transaction.atomic
    def create(self, validated_data):
        products = validated_data.pop('products')
        for new_product in products:
            product = get_object_or_404(Product, id=new_product['id'])
            new_quantity = int(new_product['quantity'])
            product_storehouse = get_object_or_404(Storehouse, product=new_product['id'])
            quantity_storehouse = product_storehouse.quantity
            if quantity_storehouse == 0:
                raise ValidationError(f'product: {product} -->> Товар закончился')
            if new_quantity > quantity_storehouse:
                raise ValidationError(f'product: {product}: quantity: Не больше {quantity_storehouse}')

            product_storehouse.quantity = product_storehouse.quantity - new_quantity
            product_storehouse.save(update_fields=['quantity'])
        order = Order.objects.create(**validated_data)
        self.create_product_quantity(order=order, products=products)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        current_products = OrderProduct.objects.filter(order=instance)
        for current in current_products:
            if current.id not in products:
                OrderProduct.objects.filter(id=current.id).delete()
        for new_product in products:
            product = get_object_or_404(Product, id=new_product['id'])
            new_quantity = int(new_product['quantity'])
            if not OrderProduct.objects.filter(order=instance, product=product).exists():
                price = Product.objects.get(id=new_product['id']).price
                OrderProduct.objects.create(
                    order=instance, product=product, price=price, quantity=new_product['quantity']
                )
            current_quantity = get_object_or_404(OrderProduct, order=instance, product=new_product['id']).quantity
            quantity_storehouse = get_object_or_404(Storehouse, id=new_product['id']).quantity
            remains = quantity_storehouse + current_quantity - new_quantity
            if remains < 0:
                raise ValidationError(f'product: {product} -->> quantity: На складе недостаточно товаров')
        self.update_storehouse(order=instance, products=products)
        instance = super().update(instance, validated_data)
        instance.products.clear()
        self.create_product_quantity(order=instance, products=products)
        instance.total_cost = OrderProduct.objects.filter(order=instance).aggregate(Sum('cost'))['cost__sum']
        instance.save()
        return instance

    def to_representation(self, instance):
        return OrderReadSerializer(instance, context=self.context).data
