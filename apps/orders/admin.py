from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.orders.models import Delivery, DeliveryType, Order, OrderProduct, Storehouse
from config.settings.base import ADMIN_EMPTY_VALUE_DISPLAY

User = get_user_model()


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    # TODO поле user
    list_display = ('id', 'address', 'phone', 'type_delivery', 'created', 'updated')
    search_fields = ('phone',)
    list_filter = ('phone', 'type_delivery')


# @admin.register(OrderProduct)
# class OrderProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'quantity', 'order', 'cost')
#     search_fields = ('order', 'product', 'quantity')
#     list_filter = ('order', 'product', 'quantity')


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'delivery', 'paid', 'total_cost', 'created', 'updated')
#     readonly_fields = ('total_cost', 'created', 'updated')
#     search_fields = ('user',)
#     list_filter = ('user',)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    raw_id_fields = ['product']
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # TODO поле user
    list_display = ('id', 'user', 'created', 'updated', 'paid', 'delivery')
    # fields = ('delivery', 'paid')
    readonly_fields = ('total_cost', 'created', 'updated')
    search_fields = ('id', 'paid')
    list_filter = ('created', 'updated', 'paid', 'delivery')
    inlines = [OrderProductInline]


@admin.register(Storehouse)
class StorehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity')
    search_fields = ('product',)
    list_filter = ('product',)
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY
