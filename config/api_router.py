from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.views import DeliveryMethodViewSet, DeliveryViewSet, OrdersViewSet, StorehouseViewSet
from apps.product.views import CategoryViewSet, ColorViewSet, MaterialViewSet, ProductViewSet
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
router.register('delivery_method', DeliveryMethodViewSet, basename='deliverymethod')
router.register('delivery', DeliveryViewSet, basename='delivery')
router.register('orders', OrdersViewSet, basename='orders')
router.register('storehouse', StorehouseViewSet, basename='deliverymethod')

app_name = 'api'
urlpatterns = router.urls
