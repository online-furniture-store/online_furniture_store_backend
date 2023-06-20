from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.product.models import Category, Color, Favorite, Material, Product
from apps.product.serializers import (
    CategorySerializer,
    ColorSerializer,
    MaterialSerializer,
    ProductSerializer,
    ShortProductSerializer,
)


class CategoryViewSet(ReadOnlyModelViewSet):
    """Вьюсет для категорий товаров."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class MaterialViewSet(ReadOnlyModelViewSet):
    """Вьюсет для материалов товаров."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    ordering_fields = ['name']


class ColorViewSet(ReadOnlyModelViewSet):
    """Вьюсет для материалов товаров."""

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    ordering_fields = ['name']


class ProductViewSet(ModelViewSet):
    """Вьюсет для товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    ordering_fields = ['name']

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            serializer = ShortProductSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            Favorite.objects.get_or_create(user=request.user, product=product)
            return Response(serializer.data, status=HTTP_201_CREATED)
        get_object_or_404(Favorite, user=request.user, product=product).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False)
    def popular(self, request):
        popular_products = Product.objects.all()[:6]  # Пока нет моделей заказов
        print(popular_products)
        # popular_products = (
        #     OrderProduct.objects
        #     .values('product__pk')
        #     .annotate(Sum('quantity'))
        #     .order_by(quantity__sum)[:6]
        # )
        serializer = ShortProductSerializer(popular_products, many=True)
        print(serializer.data)
        return Response(serializer.data)
