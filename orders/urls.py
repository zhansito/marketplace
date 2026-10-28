from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),
    path(
        "<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),
    path(
        "<int:order_id>/pay/",
        views.simulate_payment, name="simulate_payment"
    )
]