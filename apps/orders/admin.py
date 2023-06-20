# from django.contrib import admin
# from django.contrib.auth import get_user_model

# from apps.orders.models import Delivery, DeliveryType, OrderProduct, Order, Storehouse
# from config.settings.base import ADMIN_EMPTY_VALUE_DISPLAY

# User = get_user_model()


# @admin.register(DeliveryType)
# class DeliveryTypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)
#     list_filter = ('name',)


# @admin.register(Delivery)
# class DeliveryAdmin(admin.ModelAdmin):
#     # TODO поле user
#     list_display = ('id', 'address', 'phone', 'type_delivery', 'created', 'updated')
#     search_fields = ('phone',)
#     list_filter = ('phone', 'type_delivery')


# class OrderProductInline(admin.TabularInline):
#     model = OrderProduct
#     raw_id_fields = ['product']
#     # fields = ('product', 'quantity')


# class OrderAdmin(admin.ModelAdmin):
#     # TODO поле user
#     list_display = ('id', 'created', 'updated', 'paid', 'delivery')
#     # fields = ('delivery', 'paid')
#     search_fields = ('id', 'paid')
#     list_filter = ('created', 'updated', 'paid', 'delivery')
#     inlines = [OrderProductInline]


# @admin.register(Storehouse)
# class StorehouseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'quantity')
#     search_fields = ('product',)
#     list_filter = ('product',)
#     empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY


# # admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
# # admin.site.register(Delivery, DeliveryAdmin)
# admin.site.register(Order, OrderAdmin)
# # admin.site.register(Storehouse, StorehouseAdmin)
