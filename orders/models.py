import uuid
from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает обработки"
        CONFIRMED = "confirmed", "Подтвержден"
        PROCESSING = "processing", "Собирается"
        SHIPPED = "shipped", "Отправлен"
        DELIVERED = "delivered", "Доставлен"
        CANCELLED = "cancelled", "Отменен"

    order_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    shipping_address = models.TextField()
    customer_note = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Order {self.order_number}"

    @property
    def total_price(self):
        return sum(
            (item.total_price for item in self.items.all()),
            start=0,
        )

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    product_name = models.CharField(
        max_length=200,
    )
    store_name = models.CharField(
        max_length=150,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity