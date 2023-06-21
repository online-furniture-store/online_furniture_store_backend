from decimal import Decimal

from django.db.models import Max
from django.utils import timezone
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.product.models import Category, Color, Discount, Favorite, FurnitureDetails, Material, Product


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class MaterialSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Material."""

    class Meta:
        model = Material
        fields = ('id', 'name')


class ColorSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Color."""

    class Meta:
        model = Color
        fields = ('id', 'name')


class FurnitureDetailsSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели FurnitureDetails."""

    class Meta:
        model = FurnitureDetails
        fields = ('purpose', 'furniture_type', 'construction', 'swing_mechanism', 'armrest_adjustment')


class DiscountSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Discount."""

    class Meta:
        model = Discount
        fields = ('discount',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Product."""

    category = CategorySerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    material = MaterialSerializer(many=True, read_only=True)
    discount = serializers.SerializerMethodField(method_name='extract_discount')
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'material',
            'image',
            'is_favorited',
            'article',
            'name',
            'width',
            'height',
            'length',
            'weight',
            'fast_delivery',
            'country',
            'brand',
            'warranty',
            'price',
            'discount',
            'total_price',
            'description',
            'color',
        )
        read_only_fields = ('material', 'category', 'purpose', 'is_favorited')

    def is_item_related(self, product, model):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return model.objects.filter(user=request.user, product=product).exists()

    def get_is_favorited(self, product):
        return self.is_item_related(product, Favorite)

    def extract_discount(self, obj):
        """Возвращает скидку на продукт."""
        now = timezone.now()
        return obj.discounts.filter(discount_end_at__gte=now).aggregate(max_discount=Max('discount'))['max_discount']

    def calculate_total_price(self, obj):
        """Возвращает рачитанную итоговую цену товара с учётом скидки."""
        discount = self.extract_discount(obj=obj)
        if discount is None:
            return obj.price
        return obj.price * Decimal(discount / 100)


class ShortProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения товаров."""

    class Meta:
        model = Product
        fields = ('pk', 'name', 'article', 'image')
        read_only_fields = fields
