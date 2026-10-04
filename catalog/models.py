from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.CASCADE,
        related_name="products",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(
        default=0,
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name