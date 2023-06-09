from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.product.models import Category, Color, Favorite, Material, Product


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    class Meta:
        model = Category
        fields = ['name', 'slug']


class MaterialSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Material."""

    class Meta:
        model = Material
        fields = ['name']


class ColorSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Color."""

    class Meta:
        model = Color
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Product."""

    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    def is_item_related(self, product, model):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return model.objects.filter(user=request.user, product=product).exists()

    def get_is_favorited(self, product):
        return self.is_item_related(product, Favorite)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('material', 'category', 'is_favorited')


class ShortProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения избранных товаров."""

    class Meta:
        model = Product
        fields = ('pk', 'name', 'article')
        read_only_fields = ('pk', 'name', 'article')
