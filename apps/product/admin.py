from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.product.models import Category, Color, Favorite, Material, Product
from config.settings.base import ADMIN_EMPTY_VALUE_DISPLAY

User = get_user_model()


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Material)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'name', 'brand', 'price', 'category')
    search_fields = ('article', 'name', 'brand')
    list_filter = ('article', 'name')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'user')
    search_fields = ('product', 'user')
    list_filter = ('product', 'user')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Color)
class ColorsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY
