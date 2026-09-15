from django.contrib import admin

from .models import MenuItem, Order, OrderItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available", "display_order", "updated_at")
    list_filter = ("is_available",)
    search_fields = ("name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("item_name", "unit_price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at", "total")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username",)
    inlines = (OrderItemInline,)
