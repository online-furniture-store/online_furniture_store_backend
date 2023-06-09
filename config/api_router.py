from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

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

app_name = 'api'
urlpatterns = router.urls
