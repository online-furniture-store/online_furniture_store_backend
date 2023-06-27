from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.product.views import (
    CategoryViewSet,
    CollectionViewSet,
    ColorViewSet,
    DiscountViewSet,
    MaterialViewSet,
    ProductViewSet,
)
from apps.reviews.views import ReviewViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('colors', ColorViewSet, basename='colors')
router.register('categories', CategoryViewSet, basename='categories')
router.register('materials', MaterialViewSet, basename='materials')
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet, basename='collections')
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('discounts', DiscountViewSet, basename='discounts')


app_name = 'api'
urlpatterns = router.urls
