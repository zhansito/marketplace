from django.contrib import admin
from .models import ProductReview, SellerReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "created_at",
    )
    list_filter = (
        "rating",
        "created_at",
    )
    search_fields = (
        "product__name",
        "user__username",
        "comment",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = (
        "store",
        "user",
        "rating",
        "created_at",
    )
    list_filter = (
        "rating",
        "created_at",
    )
    search_fields = (
        "store__name",
        "user__username",
        "comment",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )