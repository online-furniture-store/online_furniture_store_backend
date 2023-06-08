from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.product.views import CategoriesViewSet, MaterialsViewSet, ProductViewSet
from apps.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('colors', ProductViewSet, basename='colors')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('materials', MaterialsViewSet, basename='materials')
router.register('products', ProductViewSet, basename='products')

app_name = 'api'
urlpatterns = router.urls
