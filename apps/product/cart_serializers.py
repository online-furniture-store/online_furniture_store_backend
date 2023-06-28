from django.db.models import Sum
from rest_framework import serializers

from apps.product.models import CartItem, CartModel, Product
from apps.product.serializers import ShortProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор данных о товаре в корзине."""

    product = ShortProductSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class CartItemCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания записи содержимого корзины."""

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class CartModelSerializer(serializers.ModelSerializer):
    """Сериализатор корзины пользователя."""

    total_quantity = serializers.SerializerMethodField(method_name='calculate_total_quantity')
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
    products = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = CartModel
        fields = ('total_quantity', 'total_price', 'products')

    def calculate_total_quantity(self, obj):
        return obj.cartitem_set.all().aggregate(Sum('quantity'))['quantity__sum']

    def calculate_total_price(self, obj):
        return sum(item.product.calculate_total_price() * item.quantity for item in obj.cartitem_set.all())


class CartItemDictSerializer(serializers.Serializer):
    """Сериализатор данных о товаре в корзине."""

    product = ShortProductSerializer()
    quantity = serializers.IntegerField()


class CartModelDictSerializer(serializers.Serializer):
    """Сериализатор корзины пользователя."""

    total_quantity = serializers.SerializerMethodField(method_name='calculate_total_quantity')
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
    products = CartItemDictSerializer(many=True, read_only=True)

    def calculate_total_quantity(self, obj):
        return sum(item.get('quantity') for item in obj.get('products'))

    def calculate_total_price(self, obj):
        return sum(item.get('product').calculate_total_price() * item.get('quantity') for item in obj.get('products'))


class CartItemCreateDictSerializer(serializers.Serializer):
    """Сериализатор для создания записи содержимого корзины."""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects, source='product_id')
    quantity = serializers.IntegerField(required=True, min_value=1)
