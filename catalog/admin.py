from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageLine(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "store",
        "category",
        "price",
        "quantity",
        "is_active",
    )
    list_filter = (
        "is_active",
        "category",
        "store",
    )
    search_fields = (
        "name",
        "sku",
        "store__name",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    inlines = [ProductImageLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "parent",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "alt_text",
        "created_at",
    )
    search_fields = (
        "product__name",
        "alt_text",
    )