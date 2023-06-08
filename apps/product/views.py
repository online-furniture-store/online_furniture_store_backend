from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.product.models import Categories, Colors, Favorite, Materials, Product
from apps.product.serializers import (
    CategoriesSerializer,
    ColorsSerializer,
    MaterialsSerializer,
    ProductSerializer,
    ShortProductSerializer,
)


class CategoriesViewSet(ReadOnlyModelViewSet):
    """Вьюсет для категорий товаров."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    http_method_names = ['get']


class MaterialsViewSet(ReadOnlyModelViewSet):
    """Вьюсет для материалов товаров."""

    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer
    ordering_fields = ['name']
    http_method_names = ['get']


class ColorsViewSet(ReadOnlyModelViewSet):
    """Вьюсет для материалов товаров."""

    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    ordering_fields = ['name']
    http_method_names = ['get']


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
