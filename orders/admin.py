from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product_name",
        "store_name",
        "price",
        "quantity",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "order_number",
        "user__username",
    )
    readonly_fields = (
        "order_number",
        "created_at",
        "updated_at",
        "total_price",
    )
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "store_name",
        "order",
        "price",
        "quantity",
        "total_price",
    )
    list_filter = ("store",)
    search_fields = (
        "product_name",
        "store_name",
        "order__order_number",
    )