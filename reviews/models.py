from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class ProductReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_reviews",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    comment = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_product_review_per_user",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name}: {self.rating}/5"


class SellerReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_reviews",
    )
    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    comment = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "store"],
                name="unique_seller_review_per_user",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.store.name}: {self.rating}/5"