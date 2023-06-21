from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.views import DeliveryTypeViewSet, DeliveryViewSet, OrderViewSet
from apps.product.views import CategoryViewSet, ColorViewSet, DiscountViewSet, MaterialViewSet, ProductViewSet
from apps.reviews.views import ReviewViewSet
from apps.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('colors', ColorViewSet, basename='colors')
router.register('categories', CategoryViewSet, basename='categories')
router.register('materials', MaterialViewSet, basename='materials')
router.register('products', ProductViewSet, basename='products')
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('discounts', DiscountViewSet, basename='discounts')

router.register('delivery_types', DeliveryTypeViewSet, basename='delivery_types')
router.register('delivery', DeliveryViewSet, basename='delivery')
router.register('orders', OrderViewSet, basename='orders')

app_name = 'api'
urlpatterns = router.urls
