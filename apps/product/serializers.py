import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from apps.product.models import Categories, Colors, Favorite, Materials, Product


class Base64ImageField(serializers.ImageField):
    """Сериалайзер для обработки изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Categories."""

    class Meta:
        model = Categories
        fields = ['name', 'slug']


class MaterialsSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Material."""

    class Meta:
        model = Materials
        fields = ['name']


class ColorsSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Color."""

    class Meta:
        model = Colors
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Product."""

    category = CategoriesSerializer(read_only=True)
    material = MaterialsSerializer(many=True, read_only=True)
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
