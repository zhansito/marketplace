from django.db import models
from users.models import SellerProfile


class Store(models.Model):
    seller = models.OneToOneField(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name="store",
    )
    name = models.CharField(
        max_length=150,
    )
    description = models.TextField(
        blank=True,
    )
    logo = models.ImageField(
        upload_to="stores/logos/",
        blank=True,
        null=True,
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