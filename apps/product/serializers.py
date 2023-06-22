from decimal import Decimal

from django.db.models import Max, Q
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
        """
        Возвращает True, если товар добавлен в избранное для ползователя.
        Возвращает False, если пользователь не авторизован или товар не в избранном у пользователя.
        """
        return self.is_item_related(product, Favorite)

    def extract_discount(self, obj):
        """Возвращает скидку на продукт."""
        now = timezone.now()
        return obj.discounts.filter(
            Q(discount_created_at=now, discount_end_at__gte=now)
            | Q(discount_created_at__lte=now, discount_end_at__gte=now)
        ).aggregate(max_discount=Max('discount'))['max_discount']

    def calculate_total_price(self, obj):
        """Возвращает рачитанную итоговую цену товара с учётом скидки."""
        discount = self.extract_discount(obj=obj)
        if discount is None:
            return obj.price
        return obj.price * Decimal(1 - discount / 100)


class ShortProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения товаров."""

    is_favorited = serializers.SerializerMethodField(method_name='analyze_is_favorited')
    discount = serializers.SerializerMethodField(method_name='extract_discount')
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'is_favorited', 'price', 'discount', 'total_price', 'image')

    def analyze_is_favorited(self, obj):
        """
        Возвращает True, если товар добавлен в избранное для ползователя.
        Возвращает False, если пользователь не авторизован или товар не в избранном у пользователя.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Favorite.objects.filter(user=request.user, product=obj).exists()

    def extract_discount(self, obj):
        """Возвращает скидку на продукт."""
        now = timezone.now()
        return obj.discounts.filter(
            Q(discount_created_at=now, discount_end_at__gte=now)
            | Q(discount_created_at__lte=now, discount_end_at__gte=now)
        ).aggregate(max_discount=Max('discount'))['max_discount']

    def calculate_total_price(self, obj):
        """Возвращает рачитанную итоговую цену товара с учётом скидки."""
        discount = self.extract_discount(obj=obj)
        if discount is None:
            return obj.price
        return obj.price * Decimal(1 - discount / 100)
