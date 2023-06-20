from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin

from apps.product.models import (
    CartItem,
    CartModel,
    Category,
    Color,
    Discount,
    Favorite,
    FurnitureDetails,
    Material,
    Product,
)
from config.settings.base import ADMIN_EMPTY_VALUE_DISPLAY

User = get_user_model()


@admin.register(Category)
class CategoriesAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('pk',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Material)
class MaterialsAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('pk',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(FurnitureDetails)
class FurnitureDetailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'purpose', 'furniture_type', 'construction', 'swing_mechanism', 'armrest_adjustment')
    search_fields = ('purpose', 'furniture_type', 'construction', 'swing_mechanism', 'armrest_adjustment')
    list_filter = ('purpose', 'furniture_type', 'construction', 'swing_mechanism', 'armrest_adjustment')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'article', 'name', 'brand', 'price', 'category')
    search_fields = ('article', 'name', 'brand')
    list_filter = ('article', 'name')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created_at', 'updated_at')
    search_fields = ('user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cart', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('cart', 'product')
    list_filter = ('cart', 'product')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'user')
    search_fields = ('product', 'user')
    list_filter = ('product', 'user')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Color)
class ColorsAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('pk',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'discount', 'discount_created_at', 'discount_end_at')
    search_fields = ('discount', 'discount_created_at', 'discount_end_at')
    list_filter = ('discount', 'discount_created_at', 'discount_end_at')
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY
